from typing import Callable, Union


def numeric_string_validator(
    field: str, value: str, ValidationException: Callable, error_msg: Union[str, dict]
):
    if value and not value.isnumeric():
        raise ValidationException(error_msg)
