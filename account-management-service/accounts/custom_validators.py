from django.core.exceptions import ValidationError


def numeric_string_validator(field: str, value: str, msg: str):
    if value and not value.isnumeric():
        raise ValidationError({field: msg})