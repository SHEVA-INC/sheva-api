from django.db import models

from ShevaAPI import settings
from boots.models import Boots


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    boots = models.ForeignKey(Boots, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if not self.pk:  # Якщо елемент замовлення новий
            self.price = self.product.price  # Встановлення ціни з продукту
        super().save(*args, **kwargs)
