# Generated by Django 4.2.11 on 2025-02-03 09:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boots', '0002_boots_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size',
            name='size',
            field=models.PositiveIntegerField(help_text='Choose a size between 30 and 45', validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(45)]),
        ),
    ]
