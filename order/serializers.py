from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    boots = OrderItemSerializer(source='orderitem_set', many=True)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        boots_data = validated_data.pop('orderitem_set')
        order = Order(**validated_data)
        total_amount = 0

        for boot_data in boots_data:
            # Припускаємо, що у моделі Boots є поле price
            product = boot_data['product']
            quantity = boot_data['quantity']
            total_amount += product.price * quantity

        order.total_amount = total_amount
        order.save()

        for boot_data in boots_data:
            OrderItem.objects.create(order=order, **boot_data)

        return order