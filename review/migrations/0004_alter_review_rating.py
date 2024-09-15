# Generated by Django 4.2.11 on 2024-06-14 18:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0003_remove_review_boots"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.FloatField(
                help_text="Choose a rating between 1 and 5",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
                verbose_name="Rating",
            ),
        ),
    ]
