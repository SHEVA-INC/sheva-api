# Generated by Django 4.2.11 on 2024-03-04 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boots', '0006_bootsimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boots',
            name='image',
        ),
    ]
