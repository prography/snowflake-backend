from datetime import datetime
from urllib import parse
from uuid import uuid4

import requests
from django.conf import settings

from accounts.models import User


class KakaoSocialLogin():
    social_type = 'KAKAO'
    app_key = settings.KAKAO_APP_KEY
    redirect_uri = settings.KAKAO_REDIRECT_URI
    code_request_url = 'https://kauth.kakao.com/oauth/authorize'
    access_token_request_url = 'https://kauth.kakao.com/oauth/token'
    user_data_request_url = 'https://kapi.kakao.com/v2/user/me'

    def login(self, user_data_per_field):
        if not User.objects.filter(email=user_data_per_field['email'], social=user_data_per_field['social']):
            raise AssertionError('해당 카카오 계정의 사용자는 존재하지 않습니다.')
        return User.objects.get(email=user_data_per_field['email'], social=user_data_per_field['social'])
    
    def sign_up(self, user_data_per_field):
        user = User.objects.filter(email=user_data_per_field['email'])
        if user:
            raise AssertionError(f'이미 {user.social}로 가입했습니다. {user.social}로 로그인 해주세요.')
        
        username = self._generate_unique_username()
        user = User.objects.create(
            email=user_data_per_field['email'],
            username=username,
            gender=user_data_per_field['gender'],
            social=user_data_per_field['social'],
            birth_year=user_data_per_field['birth_year'])
        return user

    def _generate_unique_username(self):
        username = uuid4().hex[:8]
        while User.objects.filter(username=username).exists():
            username = uuid4().hex[:8]
        return username

    def get_auth_url(self):
        body = {
            'client_id': self.app_key,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'account_email,gender,birthday'
        }
        query_string = '&'.join(['%s=%s' % (key, value) for (key, value) in body.items()])
        code_request_url = f'{self.code_request_url}?{query_string}'
        return code_request_url

    def get_user_data(self, request):
        code = self._get_code(request)
        access_token = self._get_access_token(code)
        user_social_data = self._get_user_social_data(access_token)
        return self._parse_user_data(user_social_data)
        
    def _get_code(self, request):
        code = request.query_params.get('code', None)
        if code is None:
            raise AssertionError('카카오 코드를 가져오는데 실패했습니다.')
        return code
    
    def _get_access_token(self, code):
        headers = {'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
        body = {
            'grant_type': "authorization_code",
            'client_id': self.app_key,
            'redirect_uri': self.redirect_uri,
            'code': code
        }

        try:
            response = requests.post(self.access_token_request_url, headers=headers, data=body)
            access_token = response.json()['access_token']
        except Exception as e:
            raise AssertionError('카카오 액세스 토큰을 가져오는데 실패했습니다.')
        return access_token

    def _get_user_social_data(self, access_token):
        headers = {'Authorization': f'Bearer {access_token}',
                   'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
        body = {'property_keys': '["properties.nickname", "properties.profile_image", "properties.thumbnail_image", "kakao_account.profile", "kakao_account.email", "kakao_account.age_range", "kakao_account.birthday", "kakao_account.gender"]'}

        response = requests.post(self.user_data_request_url, headers=headers, data=body)
        if response.status_code != 200:
            raise AssertionError('카카오 사용자 정보를 가져오는데 실패했습니다.')
        return response.json()
    
    def _parse_user_data(self, user_social_data):
        user_data_per_field = dict()

        user_data_per_field['email'] = self._get_email(user_social_data)
        user_data_per_field['gender'] = self._get_gender(user_social_data)
        user_data_per_field['social'] = self._get_social(user_social_data)
        user_data_per_field['birth_year'] = self._get_brith_year(user_social_data)

        return user_data_per_field

    def _get_email(self, data):
        try:
            return data.get('kakao_account').get('email')
        except:
            raise ValueError('이메일 정보를 받아올 수 없습니다. 카카오 계정의 권한 설정을 확인하세요.')

    def _get_gender(self, data):
        try:
            gender = data.get('kakao_account').get('gender')
        except:
            raise ValueError('성별 정보를 받아올 수 없습니다. 카카오 계정의 권한 설정을 확인하세요.')
        
        if gender == 'female':
            return 'WOMAN'
        else:
            return 'MAN'

    def _get_social(self, data):
        return self.social_type

    def _get_brith_year(self, data):
        try:
            age_range = data.get('kakao_account').get('age_range')
        except:
            raise ValueError('연령대 정보를 받아올 수 없습니다. 카카오 계정의 권한 설정을 확인하세요.')

        age = 0
        for boundary in age_range.split('~'):
            if boundary.isdecimal():
                age += int(boundary)
            else:
                age += age
        age //= 2
        birth_year = datetime.now().year - age
        return birth_year + 1

