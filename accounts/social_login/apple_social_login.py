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
            # gender=user_data_per_field['gender'],
            # birth_year=user_data_per_field['birth_year'],
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


# encoded_jwt = 'eyJraWQiOiJlWGF1bm1MIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoiY29tLnNub3dmbGFrZS5zYWZlbG92ZSIsImV4cCI6MTU5Mzg0NzMwNSwiaWF0IjoxNTkzODQ2NzA1LCJzdWIiOiIwMDE1MTAuYTc4NjdlZjJlYTVjNDExNGJkNjYxOGUxZTI1MzY0MzMuMTMzNiIsIm5vbmNlIjoiMzM0NTQ1ZmQxMDIxZWY4NmZkMzc2MDUyNmM2YzAwYzczNmZhY2Y0ZTNjMWRiMzliYzY5ZjczNWQ2NDRhY2MxOCIsImNfaGFzaCI6IldQR3J0eFAxS1AxUVRoZjFBSjhfMnciLCJlbWFpbCI6ImRlZzk4MTBAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwiYXV0aF90aW1lIjoxNTkzODQ2NzA1LCJub25jZV9zdXBwb3J0ZWQiOnRydWV9.dLwV1h8eyVKbYQ-z65Vvbw5-BYg0torulNQbW1fhvSeuvYaug8xnmQlxjk4XZwPjYz2TYQ2JQhH_2iLPF7YMfwpZMrpvxslCe69A4S-q-Sutqx5qBg9VCXhipWABUXjg2ab4WSk-zkbAsYLNb5JrjWbz6yGnmyMgYEn9gUdjSno6ZshZjTSxCocwEuwV1RmFLXfDZE8TuCC5DI3-mnI_PwrZuhfn3OBBfOeI2jRWMo-OFGTUVSONfMFVzXLoOKmFikU4S6QVaFfueO1rI5HfMD9JzgBneMpfjPvzh1kiXY8wPD9OiNhho7NWdKzcCdFxjMkfsHC3ir9m7PtlQBpCbQ'
