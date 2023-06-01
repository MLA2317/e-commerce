from rest_framework import generics, views, status
from .serializer import AccountSerializer, RegisterSerializer, LoginSerializer, ChangeNewPassword, EmailVerification,\
    ResetPassword, SetNewPassword
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .permission import IsOwnerReadOnlyForAccount
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.conf import settings
from django.urls import reverse
from drf_yasg import openapi
from ..models import Account
from .utils import Util
import jwt


class AccountRegisterView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/register/
    serializer_class = RegisterSerializer

    # user create
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # user info
        user_data = serializer.data
        user = Account.objects.get(username=user_data['username'])

        # get refresh token
        token = RefreshToken.for_user(user)

        # activate account with email
        current_site = 'localhost:8000/'
        relative_link = 'account/verify-username/'
        abs_url = f'http://' + current_site + relative_link + '?token=' + str(token.access_token)
        username_body = f'Hi, {user.username} \n User link below to activate your username \n {abs_url}'
        data = {
            'to_username': user.username,
            'username_subject': 'Activate username to Ogani Ecommerce',
            'username_body': username_body
        }
        Util.send_email(data)

        return Response({'success': True, 'message': data}, status=status.HTTP_201_CREATED)


class EmailVerificationView(APIView):
    # http://127.0.0.1:8000/account/verify-email/?token={token}/
    serializer_class = EmailVerification
    permission_classes = (AllowAny,)
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Verify username',
                                           type=openapi.TYPE_STRING)

    def get(self, request):
        token = request.GET.get('tokens')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print(payload)
            user = Account.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
                print(user)
            return Response({'success': True, 'message': 'Username successfully activated'},
                            status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as e:  # Agar tokenni muddati tugagan bolsa shu hatolik chiqadi
            return Response({'success': False, 'message': f'Verification expired | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:  # Agar notog'ri token terilgan bo'lsa shu xatolik chiqadi
            return Response({'success': False, 'message': f'Invalid token | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/login/
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Credentials is in valid'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/reset-password/
    serializer_class = ResetPassword

    def post(self, request):
        user = Account.objects.filter(username=request.data['username']).first()

        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id)) # bu url toplamga ozgatiruvchiga mos keluvchi simvollar a-z 0-9 + - _
            token = PasswordResetTokenGenerator().make_token(user) # parolni qayta tiklash un, make_token - bu parolni tiklash un
            current_site = 'localhost:8000/'
            abs_url = f'http//:{current_site}account/set-password-confirm?uidb64={uidb64}&token={token}'
            email_body = f'Hello, \n User link belowto activete your email \n {abs_url}'
            data = {
                'to_email': user.email,
                'email_subject': 'Reset password',
                'email_body': email_body
            }
            Util.send_email(data)
            return Response({'success': True, 'message': 'Link sent to email'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Email did not match '}, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordConfirmView(views.APIView): # parolni tiklash va tokenni tekshirish
    # http://127.0.0.1:8000/account/set-password-confirm/<uidb64>/<token>/
    # serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64)) # bytes ni matnga ozgartirib beradi
            user = Account.objects.filter(id=id).first() # bu userni id sini filterlab beradi
            if not PasswordResetTokenGenerator().check_token(user, token): # bu tokenni tekshiradi
                return Response({'success': False, 'message': 'Token is not valid, please try again'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

        except DjangoUnicodeDecodeError as e:
            return Response({'success': False, 'message': f'DecodeError: {e.args}'},
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response({'success': True, 'message': 'Successfully checked', 'uidb64': uidb64, 'token': token},
                        status=status.HTTP_200_OK)


class SetNewPasswordCompletedView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/set-password-completed/
    serializer_class = SetNewPassword
    permission_classes = (AllowAny,)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Credentials is invalid'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ChangePasswordCompletedView(generics.UpdateAPIView):
    # http://127.0.0.1:8000/account/change-password/
    queryset = Account.objects.all()
    serializer_class = ChangeNewPassword
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully set new password'}, status=status.HTTP_200_OK)


class MyAccountView(generics.GenericAPIView):
    # http://127.0.0.1:8000/account/login/{email}/
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsOwnerReadOnlyForAccount, IsAuthenticated)
    lookup_field = 'username'






