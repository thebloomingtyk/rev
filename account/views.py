from account.utils import Util
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import Http404, HttpResponsePermanentRedirect
import env
import json
from account.serializer import *
from account.models import *
from django.db import transaction
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        response = super(StandardResultsSetPagination,
                         self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['page_size'] = self.page_size
        return response


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class UserUpdateView(generics.GenericAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        User_key = self.get_object(self.kwargs.get('pk_user', ''))
        serializer = self.serializer_class(
            User_key, data=request.data, partial=True)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_201_CREATED
            serializer.save()
            return Response(serializer.data, status=status_code)

    def get(self, request, *args, **kwargs):
        User = self.get_object(self.kwargs.get('pk_user', ''))
        serializer = UserUpdateSerializer(User)
        return Response(serializer.data)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'email': serializer.data['email'],
                'role': serializer.data['role'],
                'name': serializer.data['name'],
                'id': serializer.data['id'],
            }

            if 'company' in serializer.data:
                response['company'] = serializer.data['company']
            if 'is_buyer_admin' in serializer.data:
                response['is_buyer_admin'] = serializer.data['is_buyer_admin']

            return Response(response, status=status_code)


# User Registration View
class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        with transaction.atomic():
            serializer = self.serializer_class(data=request.data)
            valid = serializer.is_valid(raise_exception=True)

            if valid:
                serializer.save()
                # if role is buyer = 6, organizationrep=5, crate their profiles

                user_data = serializer.data

                # send email
                user = User.objects.get(email=user_data['email'])
                serializer2 = UserRegisterSerializer(user)
                token = RefreshToken.for_user(user).access_token
                current_site = env.frontend_url
                relativeLink = 'verify-email/'
                absurl = current_site + relativeLink + str(token)
                email_body = 'Hi ' + user.first_name + \
                    ' Use the link below to verify your email \n' + absurl
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Verify your email'}
                response = {
                    'success': True,
                    'statusCode': status.HTTP_201_CREATED,
                    'message': 'User successfully registered!',
                    'user': serializer2.data,
                }

                Util.send_email(data)

                return Response(response, status=status.HTTP_201_CREATED)


# User Registration View
class UserReSendAccountActivationEmailView(generics.GenericAPIView):
    serializer_class = ResendVerificationSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = request.data.get('user', '')
        # send email
        user = User.objects.get(id=user)
        serializer2 = UserRegisterSerializer(user)
        token = RefreshToken.for_user(user).access_token
        current_site = env.frontend_url
        relativeLink = 'verify-email/'
        absurl = current_site + relativeLink + str(token)
        email_body = 'Hi ' + user.first_name + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        response = {
            'success': True,
            'statusCode': status.HTTP_201_CREATED,
            'message': 'Email successfully resent!',
            'user': serializer2.data,
        }

        Util.send_email(data)

        return Response(response, status=status.HTTP_201_CREATED)


# Email Verification  View
class VerifyEmailView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            token = serializer.data['token']

            try:
                payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms='HS256')
                user = User.objects.get(id=payload['user_id'])
                if not user.is_verified or not user.is_active:
                    user.is_verified = True
                    user.is_active = True
                    user.login_attempt = 0
                    user.save()
                serializer = UserRegisterSerializer(user)
                data = {}
                data['message'] = 'Successfully activated'
                data['uid64'] = urlsafe_base64_encode(
                    smart_bytes(user.id))
                data['token'] = PasswordResetTokenGenerator(
                ).make_token(user)
                data['email'] = user.email

                return Response(data, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.exceptions.DecodeError:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            absurl = env.frontend_url + f'reset-password/{uidb64}/{token}'
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            raise Http404


class CustomRedirect(HttpResponsePermanentRedirect):
    pass

    # allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny, )

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success': True, 'message': 'Credentials valid', 'uid64': uidb64, 'token': token}, status=status.HTTP_200_OK)
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny, )

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
