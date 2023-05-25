from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User
from .validators import validate_year

MIN_SCORE = 1
MAX_SCORE = 10


class Genre(models.Model):
    name = models.CharField(
        max_length=256, unique=True, default='Жанр отсутствует'
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(
        max_length=256, unique=True, default='Категория отсутствует'
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=256,
    )
    year = models.IntegerField(
        validators=(validate_year,), verbose_name='Год', db_index=True,
    )
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True,
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['year']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_constraint=False,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_constraint=False,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(
                MIN_SCORE, f'Вариации от {MIN_SCORE} до {MAX_SCORE}'
            ),
            MaxValueValidator(
                MAX_SCORE, f'Вариации от {MIN_SCORE} до {MAX_SCORE}'
            ),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзывы',
        on_delete=models.CASCADE,
        related_name='comments',
        db_constraint=False,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователи',
        on_delete=models.CASCADE,
        related_name='comments',
        db_constraint=False,
    )
    pub_date = models.DateTimeField(
        verbose_name='Время публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

    def __str__(self):
        return self.text
