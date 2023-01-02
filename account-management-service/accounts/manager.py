from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str = None,
    ):
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
        return account

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str
    ):
        account = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
        )
        account.is_admin = True
        account.save(using=self._db)
        return account
