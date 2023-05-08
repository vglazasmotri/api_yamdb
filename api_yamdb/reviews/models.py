from django.db import models


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
