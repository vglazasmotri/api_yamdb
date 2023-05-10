from django.db import models
from django.contrib.auth.models import AbstractUser

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE_CHOICES = (
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER),
)


class User(AbstractUser):
    username = models.SlugField(
        'Имя пользователя',
        max_length=150,
        blank=False,
        unique=True,
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
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
    confirmation_code = models.CharField('Код подтверждения', max_length=255)

    def __str__(self):
        return self.username


class Genre(models.Model):
    # PlaceHolder
    slug = models.SlugField()


class Category(models.Model):
    # PlaceHolder
    slug = models.SlugField()


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    rating = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
