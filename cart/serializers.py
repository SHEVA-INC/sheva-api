from rest_framework import serializers

from boots.serializers import BootsSerializer, BootsCartSerializer
from .models import Cart, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    product = BootsCartSerializer()

    class Meta:
        model = CartProduct
        fields = ['product', 'size', 'quantity', 'subtotal']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_representation = representation.pop('product')
        product_representation['quantity'] = representation['quantity']
        product_representation['subtotal'] = representation['subtotal']
        product_representation['size'] = instance.size
        return product_representation


class CartSerializer(serializers.ModelSerializer):
    cartproduct_set = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['cartproduct_set', 'total_price']

    def get_total_price(self, cart):
        return cart.total_price()
