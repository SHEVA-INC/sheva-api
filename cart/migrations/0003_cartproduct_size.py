# Generated by Django 4.2.11 on 2024-06-10 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartproduct",
            name="size",
            field=models.PositiveIntegerField(default=35),
        ),
    ]
