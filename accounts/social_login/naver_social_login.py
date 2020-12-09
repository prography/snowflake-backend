from uuid import uuid4

import requests
from django.conf import settings

from accounts.models import User


class NaverSocialLogin():
    social_type = 'NAVER'
    app_key = settings.NAVER_APP_KEY
    app_secret_key = settings.NAVER_APP_SECRET_KEY
    redirect_uri = settings.NAVER_REDIRECT_URI
    access_token_request_url = 'https://nid.naver.com/oauth2.0/token'
    user_data_request_url = 'https://openapi.naver.com/v1/nid/me'

    def login(self, user_data_per_field):
        if not User.objects.filter(email=user_data_per_field['email'], social=user_data_per_field['social']):
            raise AssertionError('해당 네이버 계정의 사용자는 존재하지 않습니다.')
        return User.objects.get(email=user_data_per_field['email'], social=user_data_per_field['social'])
    
    def sign_up(self, user_data_per_field):
        user = User.get_user_or_none(email=user_data_per_field['email'])
        if user:
            raise AssertionError(f'이미 {user.social}로 가입했습니다. {user.social}로 로그인 해주세요.')
        
        username = self._generate_unique_username()
        user = User.objects.create(
            email=user_data_per_field['email'],
            username=username,
            social=user_data_per_field['social'])
        return user

    def _generate_unique_username(self):
        username = uuid4().hex[:8]
        while User.objects.filter(username=username).exists():
            username = uuid4().hex[:8]
        return username

    def get_user_data(self, code, status):
        access_token_by_type = self._get_access_token_by_type(code, status)
        user_social_data = self._get_user_social_data(access_token_by_type)
        return self._parse_user_data(user_social_data)
        
    def _get_access_token_by_type(self, code, status):
        body = {
            'client_id': self.app_key,
            'client_secret': self.app_secret_key,
            'grant_type': 'authorization_code',
            'state': status,
            'code': code
        }

        query_string = '&'.join(['%s=%s' % (key, value) for (key, value) in body.items()])
        access_token_request_url = f'{self.access_token_request_url}?{query_string}'

        try:
            response = requests.get(access_token_request_url)
            access_token = response.json()['access_token']
            token_type = response.json()['token_type']
        except Exception as e:
            raise AssertionError('네이버 액세스 토큰을 가져오는데 실패했습니다. 재시도 해주세요.')
        return {
            'access_token': access_token,
            'token_type': token_type
        }

    def _get_user_social_data(self, access_token_by_type):
        headers = {'Authorization': f"{access_token_by_type['token_type']} {access_token_by_type['access_token']}"}

        response = requests.post(self.user_data_request_url, headers=headers)
        if response.status_code != 200:
            raise AssertionError('네이버 사용자 정보를 가져오는데 실패했습니다.')
        return response
        
    
    def _parse_user_data(self, user_social_data):
        user_data = user_social_data.json().get('response')
        user_data_per_field = dict()

        user_data_per_field['email'] = self._get_email(user_data)
        user_data_per_field['social'] = self._get_social()

        return user_data_per_field

    def _get_email(self, data):
        try:
            return data.get('email')
        except:
            raise ValueError('이메일 정보를 받아올 수 없습니다. 네이버 계정의 권한 설정을 확인하세요.')

    def _get_social(self):
        return self.social_type
