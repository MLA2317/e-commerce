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
    serializer_class = RegisterSerializer

    # user create
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # user info
        user_data = serializer.data
        user = Account.objects.get(email=user_data['email'])

        # get refresh token
        token = RefreshToken.for_user(user)

        # activate account with email
        current_site = 'localhost:8000/'
        relative_link = 'account/verify-email/'
        abs_url = f'http://' + current_site + relative_link + '?token=' + str(token.access_token)
        email_body = f'Hi, {user.email} \n User link below to activate your email \n {abs_url}'
        data = {
            'to_email': user.email,
            'email_subject': 'Activate email to Ogani Ecommerce',
            'email_body': email_body
        }
        Util.send_email(data)

        return Response({'success': True, 'message': 'Activate url was sent your email'}, status=status.HTTP_201_CREATED)


class EmailVerificationView(APIView):
    serializer_class = EmailVerification
    permission_classes = (AllowAny,)
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Verify email',
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
            return Response({'success': True, 'message': 'Email successfully activated'},
                            status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as e:  # Agar tokenni muddati tugagan bolsa shu hatolik chiqadi
            return Response({'success': False, 'message': f'Verification expired | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:  # Agar notog'ri token terilgan bo'lsa shu xatolik chiqadi
            return Response({'success': False, 'message': f'Invalid token | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):






