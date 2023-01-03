import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.core.validators import MinLengthValidator
from .manager import AccountManager
from .custom_validators import numeric_string_validator


class Account(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(
        max_length=11, 
        validators=[MinLengthValidator(11), numeric_string_validator]
    )
    bvn = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11), numeric_string_validator],
        unique=True,
        null=True,
        blank=True,
    )
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
