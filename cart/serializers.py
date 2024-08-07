from rest_framework import serializers

from boots.serializers import BootsCartSerializer
from .models import Cart, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    product = BootsCartSerializer()
    cart_product_id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = CartProduct
        fields = ['cart_product_id', 'product', 'size', 'quantity', 'subtotal']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_representation = representation.pop('product')
        product_representation['cart_product_id'] = representation['cart_product_id']
        product_representation['quantity'] = representation['quantity']
        product_representation['subtotal'] = representation['subtotal']
        product_representation['size'] = instance.size
        return product_representation


class CartSerializer(serializers.ModelSerializer):
    cartproduct_set = CartProductSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'cartproduct_set', 'total_price']

    def get_total_price(self, obj):
        return sum(item.subtotal for item in obj.cartproduct_set.all())