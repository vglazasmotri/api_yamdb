"""Заполняет базу данных информацией из таблиц."""

from csv import DictReader
from django.core.management import BaseCommand
from django.conf import settings

from reviews.models import Category, Comment, Genre, Review, Title, User

FILE_DIR = settings.STATICFILES_DIRS[0] / 'data'
FILE_TO_MODEL = {
    'users.csv': User,
    'category.csv': Category,
    'comments.csv': Comment,
    'genre.csv': Genre,
    'review.csv': Review,
    'titles.csv': Title,
    'genre_title.csv': Title.genre.through,
}


# Too much nesting for my taste, but it's no CPU handler
class Command(BaseCommand):
    def handle(self, *args, **options):
        for sheet_name, model in FILE_TO_MODEL.items():
            with open(FILE_DIR / sheet_name, encoding='utf-8') as data_sheet:
                reader = DictReader(data_sheet)
                for data in reader:
                    for key in ('category', 'author'):
                        if key in data:
                            data[f'{key}_id'] = data.pop(key)
                    model.objects.update_or_create(**data)
        self.stdout.write('The data from sheets imported.')
