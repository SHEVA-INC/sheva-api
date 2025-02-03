from rest_framework import serializers

from accessories.models import Accessory


class AccessoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = '__all__'


class AccessoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = ["id", "name", "price", "main_image", "type"]