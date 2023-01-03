from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



def numeric_string_validator(value: str):
    if not value.isnumeric():
        raise ValidationError(
            _("%(value)s is invalid. It should contain only digits"),
            params={"value": value},
        )
