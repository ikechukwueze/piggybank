from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status, serializers
from accounts.models import Account
from knox.models import AuthToken
from knox import crypto


class APITest(APITestCase):
    fixtures = ["accounts.json"]

    def setUp(self) -> None:
        self.account_details = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@mail.com",
            "phone_number": "12345678905",
            "password": "fakepassword",
            "confirm_password": "fakepassword",
        }
        self.account_signup_url = reverse("account_signup")
        self.account_login_url = reverse("account_login")
        self.change_password_url = reverse("change_account_password")
        self.update_bvn_url = reverse("update_bvn")

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
        self.assertEqual(response.data["last_name"], self.account_details["last_name"])
        self.assertEqual(response.data["email"], self.account_details["email"])
        self.assertNotEqual(response.data["token"], "")
        self.assertEqual(Account.objects.count(), 2)

    def test_account_signup_token(self):
        response = self.client.post(
            self.account_signup_url, self.account_details, format="json"
        )
        account_email = response.data["email"]
        response_token = response.data["token"]
        account = Account.objects.get(email=account_email)
        hashed_token = AuthToken.objects.get(user=account).digest
        self.assertEqual(hashed_token, crypto.hash_token(response_token))

    def test_account_login(self):
        login_details = {"email": "janedoe@mail.com", "password": "fakepassword"}
        response = self.client.post(
            self.account_login_url, login_details, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], login_details["email"])
        self.assertNotEqual(response.data["token"], "")
        self.assertTrue(
            AuthToken.objects.filter(user__email="janedoe@mail.com").exists()
        )

    def test_cannot_login_with_incorrect_details(self):
        login_details = {"email": "janedoe@mail.com", "password": "badfakepassword"}
        response = self.client.post(
            self.account_login_url, login_details, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        response = self.client.post(self.account_signup_url, self.account_details, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        change_password_response = self.client.patch(
            self.change_password_url,
            {"old_password": "fakepassword", "new_password": "newfakepassword"},
            format="json"
        )
        self.assertEqual(change_password_response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(change_password_response.data, {"message": "Password changed successfully"})

    def test_update_bvn(self):
        response = self.client.post(self.account_signup_url, self.account_details, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        update_bvn_response = self.client.patch(
            self.update_bvn_url,
            {"bvn": "12345678901"},
            format="json"
        )
        self.assertEqual(update_bvn_response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(update_bvn_response.data, {"message": "Bvn updated successfully"})
    
    def test_raises_exception_for_invalid_bvn(self):
        response = self.client.post(self.account_signup_url, self.account_details, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        update_bvn_response = self.client.patch(
            self.update_bvn_url,
            {"bvn": "123456789"},
            format="json"
        )
        self.assertEqual(update_bvn_response.status_code, status.HTTP_400_BAD_REQUEST)
        