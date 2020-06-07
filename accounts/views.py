import json
import uuid

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from accounts.serializers.accounts import (CustomUserObtainPairSerializer,
                                           UserSerializer)
from accounts.social_login import kakao, naver


class AnonCreateAndUpdateOwnerOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return view.action == 'create' or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return view.action in ['retrieve', 'update',
                               'partial_update'] and obj.id == request.user.id or request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    # def get_permissions(self):
    #     if self.action == 'create':
    # permission_classes = [AnonCreateAndUpdateOwnerOnly]
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    state_token_code = uuid.uuid4()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response({"message": "회원가입 완료!"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='kakao-login')
    def kakao_login(self, request, pk=None):
        app_key = settings.KAKAO_APP_KEY
        redirect_uri = settings.KAKAO_REDIRECT_URI
        url = f'https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code&scope=account_email,gender,birthday'
        return redirect(url)

    @action(detail=False, methods=['get'], url_path='kakao-login-callback')
    def kakao_login_callback(self, request, **kwargs):
        try:
            code = kakao.get_code(request)
            access_token = kakao.get_access_token(code)
            user_response = kakao.get_user_response(access_token)
            snowflake_user_data = kakao.get_data_for_snowflake(user_response.json())
        except Exception as e:
            if e.args:
                detail = e.args[0]
                error_name = e.__class__.__name__
            return Response({"message": f'{error_name}가 발생했습니다. {detail}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = self._kakao_login_or_sign_up(snowflake_user_data)
        if not isinstance(user, User):
            return Response({
                "message": f"이미 {user}로 회원가입을 하셨습니다. 다시 확인해주세요."
            })

        refresh = CustomUserObtainPairSerializer.get_token(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

    def _kakao_login_or_sign_up(self, snowflake_user_data):
        email = snowflake_user_data['email']
        social = snowflake_user_data['social']
        user = User.objects.filter(email=email)

        if user.exists():
            user = User.objects.get(email=email)
            if user.social == social:
                user = kakao.login(snowflake_user_data)
                return user
            else:
                already_signup_social = user.social
                if already_signup_social == 'NONE':
                    already_signup_social = "눈송이"
                return already_signup_social

        user = kakao.sign_up(snowflake_user_data)
        return user

    @action(detail=False, methods=['get'], url_path='naver-login')
    def naver_login(self, request, pk=None):
        state_token_code = self.state_token_code
        client_id = settings.NAVER_APP_KEY
        callback_url = settings.NAVER_REDIRECT_URI

        url = f'https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={callback_url}&state={state_token_code}'
        return redirect(url)
        
    @action(detail=False, methods=['get'], url_path='naver-login-callback')
    def naver_login_callback(self, request, **kwargs):
        callback_status_token_code = request.query_params.get('state')
        if callback_status_token_code != self.state_token_code:
            Response({'message': 'state token code is not valid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            # client_id = settings.NAVER_APP_KEY
            # client_secret = settings.NAVER_APP_SECRET_KEY
            state = self.state_token_code
            code = naver.get_code(request)
            access_token, token_type = naver.get_access_token(code, state)
            user_response = naver.get_user_response(access_token, token_type)
            snowflake_user_data = naver.get_data_for_snowflake(user_response.json())
        except Exception as e:
            if e.args:
                detail = e.args[0]
                error_name = e.__class__.__name__
            return Response({"message": f'{error_name}가 발생했습니다. {detail}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        user = self._naver_login_or_sign_up(snowflake_user_data)
        if not isinstance(user, User):
            return Response({
                "message": f"이미 {user}로 회원가입을 하셨습니다. 다시 확인해주세요."
            })
        
        refresh = CustomUserObtainPairSerializer.get_token(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    
    def _naver_login_or_sign_up(self, snowflake_user_data):
        email = snowflake_user_data['email']
        social = snowflake_user_data['social']
        user = User.objects.filter(email=email)
        
        if user.exists():
            user = User.objects.get(email=email)
            if user.social == social:
                user = naver.login(snowflake_user_data)
                return user
            else:
                already_signup_social = user.social
                if already_signup_social == 'NONE':
                    already_signup_social = "눈송이"
                return already_signup_social

        user = naver.sign_up(snowflake_user_data)
        return user
