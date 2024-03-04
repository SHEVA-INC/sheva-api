from django.db import models

from ShevaAPI import settings
from boots.models import Boots


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    boots = models.ManyToManyField(Boots, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    product = models.ForeignKey(Boots, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
