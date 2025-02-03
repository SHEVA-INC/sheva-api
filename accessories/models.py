import os
import uuid

from django.db import models

def accessory_custom_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "uploads",
        "accessory_images",
        f"{uuid.uuid4()}{extension}",
    )


class Accessory(models.Model):
    TYPE_CHOICES = [
        ("баф", "Баф"),
        ("шкарпетки", "Шкарпетки"),
        ("гетри-обрізки", "Гетри-обрізки"),
        ("щитки", "Щитки"),
        ("рукавички", "Рукавички"),
        ("мішечки", "Мішечки"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to=accessory_custom_path)
    size = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name
