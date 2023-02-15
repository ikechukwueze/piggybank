from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import Account
from .forms import AccountCreationForm, AccountChangeForm

# Register your models here.


class AccountAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = AccountChangeForm
    add_form = AccountCreationForm

    # The fields to be used in displaying the Account model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "bvn",
        "is_verified",
        "is_admin",
    )
    list_filter = (
        "is_verified",
        "is_admin",
    )
    readonly_fields = ("id",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "bvn",
                    "is_verified",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "id",
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "bvn",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    ordering = ("email",)
    search_fields = ("email",)
    filter_horizontal = ()


admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)
