from django.db import models


class Product(models.Model):
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

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=100, choices=COLOR_CHOICES)
    size = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    brand = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

