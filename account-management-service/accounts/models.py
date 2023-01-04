import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from .manager import AccountManager
from .custom_validators import numeric_string_validator


class Account(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(max_length=11)
    bvn = models.CharField(max_length=11, unique=True, null=True, blank=True)
    signup_date = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def clean(self):
        if len(self.first_name) < 2:
            raise ValidationError(
                {"first_name": "First name should have at least 2 letters"}
            )

        if len(self.last_name) < 2:
            raise ValidationError(
                {"last_name": "Last name should have at least 2 letters"}
            )

        if len(self.phone_number) != 11:
            raise ValidationError({"phone_number": "Phone number should be 11 digits"})

        if self.bvn and len(self.bvn) != 11:
            raise ValidationError({"bvn": "Bvn should be 11 digits"})

        numeric_string_validator(
            "phone_number", self.phone_number, "Phone number should contain digits only"
        )
        numeric_string_validator("bvn", self.bvn, "BVN should contain digits only")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
