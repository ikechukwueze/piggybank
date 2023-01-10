from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import SignUpSerializer, LoginSerializer, ChangePasswordSerializer, UpdateBvnSerializer
from utils.exceptions import MaximumTokensExceeded

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
            "token": token
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
                "token": token
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