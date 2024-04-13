from django.db import models
from cart.models import Cart


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    city_town = models.CharField(max_length=255)
    post_office_number = models.IntegerField()
    phone_number = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.cart.total_price()

    def __str__(self):
        return f'Order {self.id} - Cart {self.cart.id}'


