from typing import Union
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Account


class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=2, max_length=50, required=True)
    last_name = serializers.CharField(min_length=2, max_length=50, required=True)
    email = serializers.EmailField(max_length=255, required=True)
    phone_number = serializers.CharField(min_length=11, max_length=11, required=True)
    password = serializers.CharField(required=True, min_length=8, max_length=32)
    confirm_password = serializers.CharField(required=True)

    def validate_email(self, value: str) -> Union[serializers.ValidationError, str]:
        if Account.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )
        return value

    def validate_phone_number(
        self, value: str
    ) -> Union[serializers.ValidationError, str]:
        if not value.isnumeric():
            raise serializers.ValidationError(
                "Phone number should contain only digits."
            )
        return value

    def validate(self, attrs: dict) -> Union[serializers.ValidationError, dict]:
        password = attrs["password"]
        confirm_password = attrs.pop("confirm_password")
        if not password == confirm_password:
            raise serializers.ValidationError({"password": "Passwords must match."})
        else:
            validate_password(password=password, user=Account(**attrs))
        return attrs

    def create(self, validated_data: dict) -> tuple[Account, str]:
        account, token = Account.objects.create_user(**validated_data)
        return account, token


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs: dict) -> Union[serializers.ValidationError, dict]:
        account = authenticate(**attrs)
        if not account:
            raise serializers.ValidationError(
                {
                    "email": "Incorrect email or password",
                    "password": "Incorrect email or password."
                }
            )
        if not account.is_active:
            raise serializers.ValidationError(
                {"email": "This account has been suspended."}
            )
        attrs["account"] = account
        return attrs