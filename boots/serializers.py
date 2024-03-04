from rest_framework import serializers
from boots.models import Boots


class BootsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boots
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
