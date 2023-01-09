from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Account
from knox.models import AuthToken
from knox import crypto


class APITest(APITestCase):
    def setUp(self) -> None:
        self.account_details = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@mail.com",
            "phone_number": "12345678901",
            "password": "fakepassword",
            "confirm_password": "fakepassword",
        }
        self.account_signup_url = reverse("account_signup")

    def test_account_signup(self):
        response = self.client.post(
            self.account_signup_url, self.account_details, format="json"
        )
        expected_keys = ["first_name", "last_name", "email", "token"]
        for key in expected_keys:
            self.assertIn(key, response.data.keys())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["first_name"], self.account_details["first_name"]
        )
        self.assertEqual(
            response.data["last_name"], self.account_details["last_name"]
        )
        self.assertEqual(
            response.data["email"], self.account_details["email"]
        )
        self.assertNotEqual(response.data["token"], "")
        self.assertEqual(Account.objects.count(), 1)

    def test_account_signup_token(self):
        response = self.client.post(
            self.account_signup_url, self.account_details, format="json"
        )
        account_email = response.data["email"]
        response_token = response.data["token"]
        account = Account.objects.get(email=account_email)
        hashed_token = AuthToken.objects.get(user=account).digest
        self.assertEqual(hashed_token, crypto.hash_token(response_token))

