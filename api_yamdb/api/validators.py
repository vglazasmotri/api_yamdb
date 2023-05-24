from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_username(value):
    if not isinstance(value, str):
        raise ValidationError('username должен иметь тип str')
    if value.lower() == 'me':
        raise ValidationError('Имя пользователя <me> недопустимо.')
    return value


def validate_year(value):
    year = timezone.now().year
    if value > year:
        raise ValidationError('Произведение ещё не вышло!')
    return value
