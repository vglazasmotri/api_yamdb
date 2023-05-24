from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = (
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=(validate_username, UnicodeUsernameValidator())
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=254,
    )
    bio = models.TextField(
        'Биография пользователя',
        blank=True,
        null=True,
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
