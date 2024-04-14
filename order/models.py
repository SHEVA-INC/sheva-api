from django.db import models
from cart.models import Cart


class Order(models.Model):
    DELIVERY_CHOICES = [
        ("self-delivery", "Самовивіз"),
        ("delivery-man", "Кур'єр"),
    ]

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    email = models.EmailField()
    region = models.CharField(max_length=255)
    city_town = models.CharField(max_length=255)
    post_office_number = models.IntegerField()
    delivery_method = models.CharField(max_length=255, choices=DELIVERY_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.cart.total_price()

    def __str__(self):
        return f'Order {self.id} - Cart {self.cart.id}'
