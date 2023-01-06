from django.contrib.auth.models import BaseUserManager
from django.db.models import Model
from django.db import transaction
from knox.models import AuthToken


class AccountManager(BaseUserManager):
    @transaction.atomic
    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str = None,
    ) -> tuple[Model, str]:
        """
        The create user model manager method, creates a user account
        with specified details and also creates a token for 
        the newly created user account.
        """
        if not email:
            raise ValueError("Email must be provided")

        if not first_name:
            raise ValueError("First name must be provided")

        if not last_name:
            raise ValueError("Last name must be provided")

        if not phone_number:
            raise ValueError("Phone number must be provided")

        account = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        account.set_password(password)
        account.save(using=self._db)
        # create user auth token
        _, token = AuthToken.objects.create(user=account)
        return account, token

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str
    ):
        account, _ = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
        )
        account.is_admin = True
        account.save(using=self._db)
        return account