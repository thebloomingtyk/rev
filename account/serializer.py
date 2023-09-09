from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import generics, serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)
    is_buyer_admin = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        password = data['password']
        email = data['email']

        # check if email exists
        try:
            user_exists = User.objects.get(email=email)

            # if user exist
            if not user_exists.is_active:
                raise AuthenticationFailed('Account disabled, Contact admin')

            if user_exists.login_attempt < 4:
                user = authenticate(email=email, password=password)

                if user is None:  # means wrong password
                    user_exists.login_attempt = user_exists.login_attempt + 1
                    user_exists.save()

                    message = 'tries' if 5 - user_exists.login_attempt > 1 else 'try'
                    raise AuthenticationFailed(
                        f"Invalid login credentials, {5 -user_exists.login_attempt} {message} left")
            else:
                user_exists.is_active = False
                user_exists.save()
                raise AuthenticationFailed(
                    'Your account has been locked due multiple failed attempts, contact system administrator')

            try:
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)

                update_last_login(None, user)

                validation = {
                    'access': access_token,
                    'refresh': refresh_token,
                    'email': user.email,
                    'role': user.role,
                    'name': user.get_full_name(),
                    'id': user.id,

                }

                if user.role == User.BUYER:  # Buyer
                    validation.update(
                        {'company': user.buyerdetails.company.id})
                    validation.update(
                        {'is_buyer_admin': user.buyerdetails.is_buyer_admin})
                return validation

            except user.DoesNotExist:
                raise AuthenticationFailed("Invalid login credentials ")
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid login credentials ")


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'first_name': 'The First Name should only contain alphanumeric characters',
        'last_name': 'The Last Name should only contain alphanumeric characters'
    }

    class Meta:
        model = User
        fields = ['title', 'email', 'role',
                  'password', 'first_name', 'last_name', 'id']
        ref_name = 'AccountUser'

    def validate(self, attrs):
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')

        if not first_name.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages['first_name'])

        if not last_name.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages['last_name'])
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class ResendVerificationSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=255)

    class Meta:
        fields = ['email']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception:
            raise AuthenticationFailed('The reset link is invalid', 401)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'is_active', 'title', 'role']


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
