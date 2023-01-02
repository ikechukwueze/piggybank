from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def bvn_string_validator(value: str):
    if not value.isnumeric:
        raise ValidationError(
            _("%(value)s is not a valid bvn"),
            params={"value": value},
        )
    
