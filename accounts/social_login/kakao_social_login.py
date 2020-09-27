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
        if user.count():
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

    def get_auth_url(self):
        body = {
            'client_id': self.app_key,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'account_email'
        }
        query_string = '&'.join(['%s=%s' % (key, value) for (key, value) in body.items()])
        code_request_url = f'{self.code_request_url}?{query_string}'
        return code_request_url

    def get_user_data(self, access_token):
        user_social_data = self._get_user_social_data(access_token)
        return self._parse_user_data(user_social_data)
        
    def _get_user_social_data(self, access_token):
        headers = {'Authorization': f'Bearer {access_token}',
                   'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
        body = {'property_keys': '["properties.nickname", "properties.profile_image", "properties.thumbnail_image", "kakao_account.profile", "kakao_account.email"]'}

        response = requests.post(self.user_data_request_url, headers=headers, data=body)
        if response.status_code != 200:
            raise AssertionError('카카오 사용자 정보를 가져오는데 실패했습니다.')
        return response.json()
    
    def _parse_user_data(self, user_social_data):
        user_data_per_field = dict()

        user_data_per_field['email'] = self._get_email(user_social_data)
        user_data_per_field['social'] = self._get_social(user_social_data)

        return user_data_per_field

    def _get_email(self, data):
        try:
            return data.get('kakao_account').get('email')
        except:
            raise ValueError('이메일 정보를 받아올 수 없습니다. 카카오 계정의 권한 설정을 확인하세요.')

    def _get_social(self, data):
        return self.social_type
