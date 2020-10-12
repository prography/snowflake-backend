import json
from uuid import uuid4

from django.shortcuts import redirect
from rest_framework import permissions, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from accounts.models import Icon
from django.contrib.auth import get_user_model
from accounts.serializers.accounts import CustomUserObtainPairSerializer, UserSerializer
from accounts.social_login.kakao_social_login import KakaoSocialLogin
from accounts.social_login.naver_social_login import NaverSocialLogin
from accounts.social_login.apple_social_login import AppleSocialLogin

User = get_user_model()

class AnonCreateAndUpdateOwnerOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return request.method == "POST" or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
                request.method in ["GET", "PUT", "PATCH"] and obj.id == request.user.id or request.user.is_staff
        )


class UserAPIView(APIView):
    permission_classes = [AnonCreateAndUpdateOwnerOnly]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        permission_classes = [permissions.AllowAny]
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "회원가입 완료!"}, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def patch(self, request, format=None):
        user = User.objects.filter(id=request.user.id).first()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # icon 업데이트
            icon_id = request.data.get('icon', None)
            if icon_id is None:
                user.icon = None
            elif Icon.objects.filter(id=icon_id).count() > 0:
                user.icon_id = icon_id
            user.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request):
        request.user.is_active = False
        request.user.save()
        return Response("{}({})이 비활성화 되었습니다. 재활성화를 위해서는 관리자에게 문의하세요".format(request.user.email, request.user.username))


class UserSocialViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs):
        self.kakao_social_login = KakaoSocialLogin()
        self.naver_social_login = NaverSocialLogin()
        self.apple_social_login = AppleSocialLogin()
        super(UserSocialViewSet, self).__init__(**kwargs)

    @action(detail=False, methods=['post'], url_path='kakao-login-callback')
    def kakao_login_callback(self, request, pk=None):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({
                'message': 'access_token이 존재하지 않습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user_data_per_field = self.kakao_social_login.get_user_data(access_token)
        user = User.get_user_or_none(email=user_data_per_field['email'])
        
        if user:
            user_login_type = user.social
            refresh = CustomUserObtainPairSerializer.get_token(user)

            return Response({
                'message': f'이미 {user_login_type}로 가입했어요. {user_login_type}로 로그인합니다.',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })

        user = self.kakao_social_login.sign_up(user_data_per_field)
        refresh = CustomUserObtainPairSerializer.get_token(user)

        return Response({
            'message': f'{user.social}로 로그인합니다.',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post'], url_path='naver-login-callback')
    def naver_login_callback(self, request, pk=None):
        code = request.data.get('code')
        state = request.data.get('state')

        not_exist_field = list()
        if code is None:
            not_exist_field.append('code')
        if state is None:
            not_exist_field.append('state')
        if not_exist_field:
            return Response({
                'message': ','.join(not_exist_field) + '이/가 존재하지 않습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user_data_per_field = self.naver_social_login.get_user_data(code, state)
        user = User.get_user_or_none(email=user_data_per_field['email'])

        if user:
            user_login_type = user.social
            refresh = CustomUserObtainPairSerializer.get_token(user)

            return Response({
                'message': f'이미 {user_login_type}로 가입했어요. {user_login_type}로 로그인합니다.',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })

        user = self.naver_social_login.sign_up(user_data_per_field)
        refresh = CustomUserObtainPairSerializer.get_token(user)

        return Response({
            'message': f'{user.social}로 로그인합니다.',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='apple-login-callback')
    def apple_login_callback(self, request, pk=None):
        identity_token = request.data.get('identity_token')
        if not identity_token:
            return Response({
                'message': 'identity_token이 존재하지 않습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user_data_per_field = self.apple_social_login.get_user_data(identity_token)

        user = User.objects.filter(email=user_data_per_field['email'])
        if user.count() == 1:
            user = User.objects.get(email=user_data_per_field['email'])
            user_login_type = user.social
            refresh = CustomUserObtainPairSerializer.get_token(user)

            return Response({
                'message': f'이미 {user_login_type}로 가입했어요. {user_login_type}로 로그인합니다.',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        
        user = self.apple_social_login.sign_up(user_data_per_field)
        refresh = CustomUserObtainPairSerializer.get_token(user)

        return Response({
            'message': f'{user.social}로 로그인합니다.',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', ])
@permission_classes([permissions.AllowAny])
def check_duplicates_email(request):
    if request.method == 'GET':
        email = request.query_params.get('value')
        if email is None:
            return Response({"message": "email is required :("})

        is_exist = User.objects.filter(email=email).count() > 0
        if is_exist:
            return Response({"message": "email {} already exist".format(email)},
                            status=status.HTTP_409_CONFLICT)

        return Response({"message": "no email duplicates :)"})


@api_view(['GET', ])
@permission_classes([permissions.AllowAny])
def check_duplicates_username(request):
    if request.method == 'GET':
        username = request.query_params.get('value')
        if username is None:
            return Response({"message": "username is required :("})

        is_exist = User.objects.filter(username=username).count() > 0
        if is_exist:
            return Response({"message": "username {} already exist".format(username)},
                            status=status.HTTP_409_CONFLICT)

        return Response({"message": "no username duplicates :)"})
