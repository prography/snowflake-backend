import jwt
from datetime import datetime
from uuid import uuid4

import requests
from django.conf import settings

from accounts.models import User


class AppleSocialLogin():
    social_type = 'APPLE'

    def login(self, user_data_per_field):
        if not User.objects.filter(email=user_data_per_field['email'], social=user_data_per_field['social']):
            raise AssertionError('해당 애플 계정의 사용자는 존재하지 않습니다.')
        return User.objects.get(email=user_data_per_field['email'], social=user_data_per_field['social'])

    def sign_up(self, user_data_per_field):
        user = User.objects.filter(email=user_data_per_field['email'])
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

    def get_user_data(self, identity_token):
        encoded_jwt = identity_token
        payload = jwt.decode(encoded_jwt, verify=False)
        return self._parse_payload(payload)

    def _parse_payload(self, payload):
        user_data_per_field = dict()

        user_data_per_field['email'] = self._get_email(payload)
        user_data_per_field['social'] = self.social_type

        return user_data_per_field

    def _get_email(self, payload):
        try:
            if not payload['email_verified']:
                raise AssertionError('애플 계정 이메일 인증을 확인해주세요.')
            return payload['email']
        except KeyError as e:
            raise AssertionError('애플 로그인 중 이메일을 가져올 수 없습니다.')
