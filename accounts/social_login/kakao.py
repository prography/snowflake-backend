from datetime import datetime
from uuid import uuid4

import environ
import requests
from django.conf import settings

from accounts.models import User


def get_code(request):
    code = request.query_params.get('code', None)
    if code is None:
        raise ValueError('카카오 코드를 가져오는데 실패했습니다.')
    return code


def get_access_token(code):
    grant_type = "authorization_code"
    app_key = settings.KAKAO_APP_KEY
    redirect_uri = settings.KAKAO_REDIRECT_URI

    url = 'https://kauth.kakao.com/oauth/token'
    headers = {'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
    body = {'grant_type': grant_type,
            'client_id': app_key,
            'redirect_uri': redirect_uri,
            'code': code}

    try:
        response = requests.post(url, headers=headers, data=body)
        access_token = response.json()['access_token']
    except Exception as e:
        raise AssertionError('카카오 액세스 토큰을 가져오는데 실패했습니다.')
    return access_token


def get_user_response(access_token):
    url = 'https://kapi.kakao.com/v2/user/me'
    headers = {'Authorization': f'Bearer {access_token}',
               'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
    body = {'property_keys': '["properties.nickname", "properties.profile_image", "properties.thumbnail_image", "kakao_account.profile", "kakao_account.email", "kakao_account.age_range", "kakao_account.birthday", "kakao_account.gender"]'}

    response = requests.post(url, headers=headers, data=body)
    if response.status_code != 200:
        raise AssertionError('카카오 사용자 정보를 가져오는데 실패했습니다.')
    return response


def get_data_for_snowflake(user_data):
    if user_data.get('kakao_account') is None:
        raise AssertionError('카카오톡 계정 정보를 읽어올 수 없습니다. 권한 설정을 확인하세요.')
    return parse_response(user_data)

def parse_response(user_data):
    user_field = dict()

    user_field['email'] = user_data.get('kakao_account').get('email', None)
    user_field['gender'] = convert_gender(
        user_data.get('kakao_account').get('gender', None))
    user_field['social'] = 'KAKAO'
    user_field['birth_year'] = 0

    age_range = user_data.get('kakao_account').get('age_range', None)

    if user_field['email'] is None:
        raise ValueError('이메일 정보를 받아올 수 없습니다. 권한 설정을 확인하세요.')

    if age_range:
        birth_year = get_user_birth_year(age_range)
        user_field['birth_year'] = birth_year

    return user_field

def convert_gender(gender):
    if gender == 'male':
        return 'MAN'
    elif gender == 'female':
        return 'WOMAN'

def get_user_birth_year(age_range):
    age = 0

    for boundary in age_range.split('~'):
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
