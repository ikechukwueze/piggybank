from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_bytes,
)
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    UpdateBvnSerializer,
    ForgotPasswordSerializer,
)
from utils.exceptions import MaximumTokensExceeded
from .models import Account

# Create your views here.


class AccountSignUpView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account, token = serializer.save()
        account_details = {
            "first_name": account.first_name,
            "last_name": account.last_name,
            "email": account.email,
            "token": token,
        }
        return Response(account_details, status=status.HTTP_201_CREATED)


class AccountLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data["account"]
        try:
            token = account.get_token()
        except MaximumTokensExceeded:
            return Response(
                {"error": "Maximum amount of tokens allowed per user exceeded."},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            account_details = {
                "first_name": account.first_name,
                "last_name": account.last_name,
                "email": account.email,
                "token": token,
            }
            return Response(account_details, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        account = self.request.user
        serializer = ChangePasswordSerializer(
            instance=account, data=request.data, context={"account": account}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_202_ACCEPTED,
        )


class ForgotPasswordView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data
        account = Account.objects.get(email=email)
        encoded_account_id = urlsafe_base64_encode(smart_bytes(account.id))
        password_reset_token = PasswordResetTokenGenerator().make_token(account)
        current_site = get_current_site(request=request).domain
        relative_link = reverse(
            "email-password-reset",
            kwargs={
                "encoded-account-id": encoded_account_id,
                "password-reset-token": password_reset_token,
            },
        )
        absolute_url = "http://" + current_site + relative_link
        print(absolute_url)
        return Response(
            {"message": "Password reset email sent."}, status=status.HTTP_200_OK
        )


class UpdateBvnView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        account = self.request.user
        serializer = UpdateBvnSerializer(
            instance=account, data=request.data, context={"account": account}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Bvn updated successfully"},
            status=status.HTTP_202_ACCEPTED,
        )
