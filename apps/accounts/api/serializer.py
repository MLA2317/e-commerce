from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from ..models import Account


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=16, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=16, write_only=True)

    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'full_name', 'avatar', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({
                'success': False, 'message': "Password didn't match, Please Try again!"
            })
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=60, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):
        user = Account.objects.filter(username=obj.get('username')).first()
        return user.tokens

    class Meta:
        model = Account
        fields = ('username', 'password', 'tokens')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed({
                'message': 'Username or password is not correct'
            })
        if not user.is_active:
            raise AuthenticationFailed({
                'message': 'Account disable'
            })

        data = {
            'success': True,
            'username': user.username,
            'tokens': user.tokens,
        }
        return data


class EmailVerification(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Account
        fields = ('tokens',)


class ResetPassword(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = Account
        fields = ('username',)


class SetNewPassword(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=30, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=30, write_only=True)
    uidb64 = serializers.CharField(max_length=60, required=True)
    token = serializers.CharField(max_length=250, required=True)

    class Meta:
        model = Account
        fields = ('password', 'password2', 'uidb64', 'token')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        _id = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.filter(id=_id).first()
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed({'success': False, 'message': 'The token is not valid'})
        if password != password2:
            raise serializers.ValidationError(
                {'success': False, 'message': 'Password did not match, please try again new'})
        user.set_password(password)
        user.save()
        return user


class ChangeNewPassword(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=6, max_length=30, write_only=True)
    password = serializers.CharField(min_length=6, max_length=30, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=30, write_only=True)

    class Meta:
        model = Account
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {'success': False, "message": "Old password did not match, please try again new"}
            )
        if password != password2:
            raise serializers.ValidationError(
                {"success": False, "message": "Password did not match, please try again new"}
            )
        user.set_password(password)
        user.save()
        return attrs


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'full_name', 'avatar', 'bio', 'is_superuser', 'is_staff', 'is_active', 'date_login')





