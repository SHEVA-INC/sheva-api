from rest_framework import serializers
from boots.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "color",
            "size",
            "stock",
            "brand"
        )
