from django.db import models

from ShevaAPI import settings
from boots.models import Boots


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Boots, related_name="boots",
                                      through='CartProduct')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        total = 0
        for cart_product in self.cartproduct_set.all():
            total += cart_product.quantity * cart_product.product.price
        return total

    def __str__(self):
        products_details = []
        for cart_product in self.cartproduct_set.all():
            product = cart_product.product
            products_details.append(
                f"{product.name} - {product.brand} (Розмір: {product.size})\n"
                f"Кількість: {cart_product.quantity}\n"
                f"Ціна за од.: ({product.price}₴)\n"
                f"------------------------------------\n")

        return f' Products: \n{"".join(products_details)}\n'


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Boots, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Cart {self.cart.id}'
