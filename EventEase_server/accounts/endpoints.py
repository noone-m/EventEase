from django.urls import path,include
from .views import (Login,log_out,Register,UserViewSet,VerifyOTP,GenerateOTP,ListOTP,DestroyOTP,
ChangePasswordRequested, ChangePassowrdRequests, UpdatePassword,VerifyEmail,GenerateVerificationLink,
ListEmailVerified)

from services.views import UserFavoriteServices

from wallet.views import RetrieveWalletAPIView,RetrieveMyWalletAPIView,DebitWalletView,CreditWalletView,TransactionsAPIView

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('register/', Register.as_view(), name = 'register'),
    path('code-generate', GenerateOTP.as_view(), name = 'generate-code'),
    path('code-verify/', VerifyOTP.as_view(), name = 'verify-code'),
    path('log-in/', Login.as_view(), name='login'),
    path('log-out/', log_out),
    path('otps', ListOTP.as_view()),
    path('destroy-code/<int:id>', DestroyOTP.as_view()),
    path('change-password-request/', ChangePasswordRequested.as_view()),
    path('change-password-requests', ChangePassowrdRequests.as_view()),
    path('update-password/', UpdatePassword.as_view()),
    path('users/favorite-services/', UserFavoriteServices.as_view()),
    path('verification-link', GenerateVerificationLink.as_view()),
    path('verify-email/', VerifyEmail.as_view()),
    path('list-verification-tokens/', ListEmailVerified.as_view()),

    path('my-wallet/', RetrieveMyWalletAPIView.as_view()),
    path('my-wallet/credit/', CreditWalletView.as_view()),
    path('my-wallet/debit/', DebitWalletView.as_view()),
    path('users/<int:user_id>/wallet/', RetrieveWalletAPIView.as_view()),

    path('transactions/', TransactionsAPIView.as_view()),

    path('',include(router.urls)),
] 