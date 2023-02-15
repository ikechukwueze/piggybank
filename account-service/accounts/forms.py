from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Account


class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Account
        fields = ("email", "first_name", "last_name", "phone_number", "bvn")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        account = super().save(commit=False)
        account.set_password(self.cleaned_data["password1"])
        if commit:
            account.save()
        return account


class AccountChangeForm(forms.ModelForm):
    """A form for updating accounts. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "bvn",
            "is_verified",
            "is_active",
            "is_admin",
        )
