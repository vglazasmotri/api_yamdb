from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    year = timezone.now().year
    if value > year:
        raise ValidationError('Произведение ещё не вышло!')
    return value
