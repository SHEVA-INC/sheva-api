from django.db import models
from cart.models import Cart


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()
    region = models.CharField(max_length=255)
    city_town = models.CharField(max_length=255)
    post_office_number = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255, default="Оплатити при отриманні")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - Cart {self.cart.id}'
