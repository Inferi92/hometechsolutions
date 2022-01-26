# Generated by Django 4.0.1 on 2022-01-26 21:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('htsolutions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ean',
            field=models.PositiveIntegerField(default=1, unique=True, validators=[django.core.validators.MaxValueValidator(9999999999999, message=None), django.core.validators.MinValueValidator(1, message=None), django.core.validators.MinLengthValidator(13, message=None)]),
        ),
    ]
