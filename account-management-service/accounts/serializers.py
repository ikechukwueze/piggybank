from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .custom_validators import numeric_string_validator
from .models import Account


class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=2, max_length=50, required=True)
    last_name = serializers.CharField(min_length=2, max_length=50, required=True)
    email = serializers.EmailField(
        max_length=255,
        required=True,
        validators=[UniqueValidator(queryset=Account.objects.all())],
    )
    phone_number = serializers.CharField(min_length=11, max_length=11, required=True)
    password = serializers.CharField(required=True, min_length=8, max_length=32)
    confirm_password = serializers.CharField(required=True)

    def validate_phone_number(self, value: str) -> str:
        numeric_string_validator(
            "phone_number",
            value,
            serializers.ValidationError,
            "Phone number should contain digits only",
        )
        return value

    def validate(self, attrs: dict) -> dict:
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