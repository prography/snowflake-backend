from datetime import datetime
from uuid import uuid4

import environ
import requests
from django.conf import settings

from accounts.models import User


def get_code(request):
    code = request.query_params.get('code', None)
    if code is None:
        raise ValueError('네이버 코드를 가져오는데 실패했습니다.')
    return code

def get_access_token(code, state):
    url = f'https://nid.naver.com/oauth2.0/token?client_id={settings.NAVER_APP_KEY}&client_secret={settings.NAVER_APP_SECRET_KEY}&grant_type=authorization_code&state={state}&code={code}'

    try:
        response = requests.get(url)
        access_token = response.json()['access_token']
        token_type = response.json()['token_type']
    except Exception as e:
        raise AssertionError('네이버 액세스 토큰을 가져오는데 실패했습니다.')
    return access_token, token_type

def get_user_response(access_token, token_type):
    url = 'https://openapi.naver.com/v1/nid/me'
    headers = {'Authorization': f'{token_type} {access_token}'}
    
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        raise AssertionError('네이버 사용자 정보를 가져오는데 실패했습니다.')
    return response

def get_data_for_snowflake(user_data):
    if user_data.get('message') is None:
        raise AssertionError('네이버 계정 정보를 읽어올 수 없습니다. 권한 설정을 확인하세요.')
    return parse_response(user_data)

def parse_response(user_data):
    user_data = user_data.get('response')

    user_field = dict()
    user_field['email'] = user_data.get('email')
    user_field['gender'] = convert_gender(user_data.get('gender'))
    user_field['social'] = 'NAVER'
    user_field['birth_year'] = get_user_birth_year(user_data.get('age'))
    return user_field

def convert_gender(gender):
    if gender == 'M':
        return 'MAN'
    elif gender == 'F':
        return 'WOMAN'

def get_user_birth_year(age_range):
    age = 0
    for boundary in age_range.split('-'):
        if boundary.isdecimal():
            age += int(boundary)
        else:
            age += age
    age //= 2
    birth_year = datetime.now().year - age
    return birth_year + 1

def sign_up(snowflake_user_data):
    username = uuid4().hex[:8]
    while User.objects.filter(username=username).exists():
        username = uuid4().hex[:8]

    user = User.objects.create(
        email=snowflake_user_data['email'],
        username=username,
        gender=snowflake_user_data['gender'],
        social=snowflake_user_data['social'],
        birth_year=snowflake_user_data['birth_year'])
    return user

def login(snowflake_user_data):
    user = User.objects.get(
        email=snowflake_user_data['email'], social=snowflake_user_data['social'])
    return user
