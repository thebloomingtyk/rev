from django.urls import path
from account.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # other auth
    path('login/', UserLoginView.as_view(), name='login'),
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<str:pk_user>/', UserUpdateView.as_view(), name='user-update'),
    path('register/', UserRegistrationView.as_view(), name='register talent'),
    path('email-verify/', VerifyEmailView.as_view(), name='email-verify'),
    path('resend-account-verify-email/',
         UserReSendAccountActivationEmailView.as_view(), name='email-verify'),
    path('request-password-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-password-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),

]
