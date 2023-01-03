from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from accounts.models import Account


# Create your tests here.


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.account_details = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@email.com",
            "phone_number": "08123456789",
            "password": "easypassword",
        }

        self.field_max_lengths = {
            "first_name": 50,
            "last_name": 50,
            "email": 255,
            "phone_number": 11,
            "bvn": 11,
        }

    def test_model_field_max_length(self):
        for field, max_length in self.field_max_lengths.items():
            self.assertEquals(Account._meta.get_field(field).max_length, max_length)

    def test_create_superuser_account(self):
        superuser_account = Account.objects.create_superuser(**self.account_details)
        self.assertEqual(Account.objects.count(), 1)
        self.account_details.pop("password")
        for field, value in self.account_details.items():
            self.assertEqual(getattr(superuser_account, field), value)
        self.assertTrue(superuser_account.is_admin)

    def test_create_account(self):
        account = Account.objects.create(**self.account_details)
        self.assertEqual(Account.objects.count(), 1)
        self.account_details.pop("password")
        for field, value in self.account_details.items():
            self.assertEqual(getattr(account, field), value)
