# models.py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from ShevaAPI import settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.subtotal() for item in self.cartitems.all())

    def clear(self):
        self.cartitems.all().delete()

    def __str__(self):
        items_details = []
        for item in self.cartitems.all():
            product = item.content_object
            size_info = f"Розмір: {item.size}" if item.size else ""
            items_details.append(
                f"{product.name} - {size_info}\n"
                f"Кількість: {item.quantity}\n"
                f"Ціна за од.: ({product.price}₴)\n"
                f"------------------------------------\n"
            )
        return f'Products: \n{"".join(items_details)}\n'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartitems', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField(null=True, blank=True)  # Optional, for boots only

    def subtotal(self):
        return self.quantity * self.content_object.price

    def __str__(self):
        size_info = f" (Size: {self.size})" if self.size else ""
        return f'{self.quantity} x {self.content_object.name}{size_info}'