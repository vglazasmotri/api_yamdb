# Generated by Django 3.2 on 2023-05-19 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230511_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.IntegerField(default=None, null=True, verbose_name='Рейтинг'),
        ),
    ]
