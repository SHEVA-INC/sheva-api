from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'cart', 'full_name', 'phone_number', 'email', 'region', 'city_town', 'post_office_number', 'payment_method', 'total_price', 'created_at']

    def validate(self, data):
        return data
