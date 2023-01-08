from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from knox.models import AuthToken
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
        account, _ = Account.objects.create_user(**self.account_details)
        self.assertEqual(Account.objects.count(), 1)
        password = self.account_details.pop("password")
        for field, value in self.account_details.items():
            self.assertEqual(getattr(account, field), value)
        self.assertTrue(check_password(password, account.password))

    def test_first_name_with_invalid_min_length_raises_exception(self):
        self.account_details["first_name"] = "J"
        with self.assertRaisesMessage(
            ValidationError, "First name should have at least 2 letters"
        ):
            Account.objects.create_user(**self.account_details)

    def test_last_name_with_invalid_min_length_raises_exception(self):
        self.account_details["last_name"] = "J"
        with self.assertRaisesMessage(
            ValidationError, "Last name should have at least 2 letters"
        ):
            Account.objects.create_user(**self.account_details)

    def test_phone_number_with_invalid_length_raises_exception(self):
        # phone number len less than 11
        self.account_details["phone_number"] = self.account_details["phone_number"][:10]
        with self.assertRaisesMessage(
            ValidationError, "Phone number should be 11 digits"
        ):
            Account.objects.create_user(**self.account_details)

        # phone number len greater than 11
        self.account_details["phone_number"] = (
            self.account_details["phone_number"] + "1234"
        )
        with self.assertRaisesMessage(
            ValidationError, "Phone number should be 11 digits"
        ):
            Account.objects.create_user(**self.account_details)

    def test_non_numeric_phone_number_raises_exception(self):
        self.account_details["phone_number"] = (
            self.account_details["phone_number"][:10] + "k"
        )
        with self.assertRaisesMessage(
            ValidationError, "Phone number should contain digits only"
        ):
            Account.objects.create_user(**self.account_details)

    def test_bvn_with_invalid_length_raises_exception(self):
        # bvn len less than 11
        self.account_details["bvn"] = "1234567890"
        with self.assertRaisesMessage(ValidationError, "BVN should be 11 digits"):
            Account.objects.create_user(**self.account_details)

        # bvn len greater than 11
        self.account_details["bvn"] = self.account_details["bvn"] + "1234"
        with self.assertRaisesMessage(ValidationError, "BVN should be 11 digits"):
            Account.objects.create_user(**self.account_details)

    def test_non_numeric_bvn_raises_exception(self):
        self.account_details["bvn"] = "1234567890k"
        with self.assertRaisesMessage(
            ValidationError, "BVN should contain digits only"
        ):
            Account.objects.create_user(**self.account_details)
