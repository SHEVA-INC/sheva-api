import os
import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


def boots_custom_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "uploads",
        "boots_images",
        f"{uuid.uuid4()}{extension}",
    )


class Boots(models.Model):
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('black', 'Black'),
        ('white', 'White'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('orange', 'Orange'),
        ('another', 'Another'),
    ]

    BRAND_CHOICES = [
        ('adidas', 'Adidas'),
        ('nike', 'Nike'),
        ('puma', 'Puma'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=100, choices=COLOR_CHOICES)
    brand = models.CharField(max_length=100, choices=BRAND_CHOICES)
    main_image = models.ImageField(upload_to=boots_custom_path)
    new = models.BooleanField(default=True)
    popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Size(models.Model):
    boots = models.ForeignKey(Boots, related_name='sizes', on_delete=models.CASCADE)
    size = models.PositiveIntegerField(validators=[
        MinValueValidator(35),
        MaxValueValidator(45)
    ], help_text='Choose a size between 35 and 45')
    stock = models.PositiveIntegerField(help_text="Stock available for this size")

    def __str__(self):
        return f"{self.boots.name} - Size {self.size}"


class BootsImage(models.Model):
    boots = models.ForeignKey(Boots, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=boots_custom_path)


    def __str__(self):
        return f"{self.boots.name} Image"
