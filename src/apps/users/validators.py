from rest_framework.exceptions import ValidationError


def phone_validate(phone_number: str) -> None:
    if len(phone_number) != 13 or not phone_number.startswith('+998') or not phone_number[1:].isdigit():
        raise ValidationError('Invalid phone number format. Phone number must start with +998 and contain only digits.') 