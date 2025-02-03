from rest_framework import serializers
from boots.models import Boots
from accessories.models import Accessory
from cart.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    product_type = serializers.SerializerMethodField()
    product_data = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_type', 'product_data', 'quantity', 'size', 'subtotal']

    def get_product_type(self, obj):
        return obj.content_type.model

    def get_product_data(self, obj):
        if isinstance(obj.content_object, Boots):
            return {
                'id': obj.content_object.id,
                'name': obj.content_object.name,
                'price': obj.content_object.price,
                'brand': obj.content_object.brand,
                'color': obj.content_object.color,
                'main_image': self.context['request'].build_absolute_uri(
                    obj.content_object.main_image.url) if obj.content_object.main_image else None,
            }
        elif isinstance(obj.content_object, Accessory):
            return {
                'id': obj.content_object.id,
                'name': obj.content_object.name,
                'price': obj.content_object.price,
                'size': obj.content_object.size,
                'type': obj.content_object.type,
                'main_image': self.context['request'].build_absolute_uri(
                    obj.content_object.main_image.url) if obj.content_object.main_image else None,
            }


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitems', many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']