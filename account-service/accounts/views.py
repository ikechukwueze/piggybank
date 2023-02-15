from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    UpdateBvnSerializer,
    RequestPasswordResetSerializer,
    ResetPasswordSerializer,
)
from utils.helpers import FernetCryptography
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


class RequestPasswordResetView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            pass
        else:
            password_reset_token = PasswordResetTokenGenerator().make_token(account)
            encrypted_user_id = FernetCryptography().encrypt(str(account.id))
            relative_url_kwargs = {
                "encrypted_user_id": encrypted_user_id,
                "password_reset_token": password_reset_token,
            }
            current_site = get_current_site(request=request).domain
            relative_url = reverse("password-reset", kwargs=relative_url_kwargs)
            password_reset_link = (
                f"http://{current_site}{relative_url}"  # email password rest link
            )
            print(password_reset_link)

        return Response(
            {"message": "A password reset link has been sent to your email."},
            status=status.HTTP_200_OK,
        )


class PasswordResetView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, **kwargs):
        encrypted_user_id = kwargs["encrypted_user_id"]
        password_reset_token = kwargs["password_reset_token"]
        decrypted_user_id = FernetCryptography().decrypt(encrypted_user_id)
        
        if not decrypted_user_id:
            raise AuthenticationFailed(detail="Invalid password reset link")
        
        try:
            account = Account.objects.get(id=decrypted_user_id)
        except Account.DoesNotExist:
            raise AuthenticationFailed(detail="Invalid password reset link")
        else:
            valid_token = PasswordResetTokenGenerator().check_token(account, password_reset_token)
        
        if not valid_token:
            raise AuthenticationFailed(detail="Invalid password reset link")
        
        return redirect('http://stackoverflow.com/')
        
        


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
