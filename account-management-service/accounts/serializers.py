from typing import Union
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
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
                    "password": "Incorrect email or password.",
                }
            )
        if not account.is_active:
            raise serializers.ValidationError(
                {"email": "This account has been suspended."}
            )
        attrs["account"] = account
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value: str) -> Union[serializers.ValidationError, dict]:
        account = self.context["account"]
        if not account.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def validate_new_password(self, value: str):
        account = self.context["account"]
        validate_password(password=value, user=account)
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, )

    def validate_email(self, value):
        try:
            Account.objects.get(email=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError({'error': 'Account with email does not exist.'})
        else:
            return value


class UpdateBvnSerializer(serializers.Serializer):
    bvn = serializers.CharField(required=True, min_length=11, max_length=11)

    def validate_bvn(
        self, value: str
    ) -> Union[serializers.ValidationError, str]:
        if not value.isnumeric():
            raise serializers.ValidationError(
                "Bvn should contain only digits."
            )
        return value

    def update(self, instance, validated_data):
        instance.bvn = validated_data["bvn"]
        instance.save()
        return instance