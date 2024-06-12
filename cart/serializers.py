from rest_framework import serializers

from boots.serializers import BootsSerializer, BootsCartSerializer
from .models import Cart, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    product = BootsCartSerializer()

    class Meta:
        model = CartProduct
        fields = ['cart', 'product', 'size', 'quantity', 'subtotal']


class CartSerializer(serializers.ModelSerializer):
    cartproduct_set = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['cartproduct_set', 'total_price']

    def get_total_price(self, cart):
        return cart.total_price()
