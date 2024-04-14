from rest_framework import serializers

from boots.serializers import BootsSerializer
from .models import Cart, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    product = BootsSerializer()

    class Meta:
        model = CartProduct
        fields = ['id', 'quantity', 'product']


class CartSerializer(serializers.ModelSerializer):
    cartproduct_set = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['cartproduct_set', 'total_price']

    def get_total_price(self, cart):
        return cart.total_price()
