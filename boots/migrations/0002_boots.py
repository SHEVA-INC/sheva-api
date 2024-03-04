# Generated by Django 4.2.11 on 2024-03-04 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('color', models.CharField(choices=[('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('black', 'Black'), ('white', 'White'), ('yellow', 'Yellow'), ('purple', 'Purple'), ('orange', 'Orange'), ('another', 'Another')], max_length=100)),
                ('size', models.PositiveIntegerField()),
                ('stock', models.PositiveIntegerField()),
                ('brand', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='product_images/')),
            ],
        ),
    ]
