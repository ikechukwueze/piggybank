from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer

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
        return Response(account_details, status=status.HTTP_200_OK)
