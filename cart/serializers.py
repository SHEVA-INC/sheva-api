from rest_framework import serializers

from boots.serializers import BootsSerializer
from .models import Cart, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    product = BootsSerializer()

    class Meta:
        model = CartProduct
        fields = ('id', 'cart', 'product', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'products', 'total_price', 'created_at')
