from rest_framework import serializers
from boots.models import Boots, BootsImage


class BootsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BootsImage
        fields = ("image",)


class BootsSerializer(serializers.ModelSerializer):
    images = BootsImageSerializer(many=True)
    uploaded_images = serializers.ListField(child= serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True)

    class Meta:
        model = Boots
        fields = (
            "id",
            "name",
            "price",
            "color",
            "size",
            "brand",
            "images",
            "uploaded_images",
        )

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        boots = Boots.objects.create(**validated_data)
        for image in uploaded_images:
            BootsImage.objects.create(boots=boots, image=image)

        return boots


class BootsDetailSerializer(serializers.ModelSerializer):
    images = BootsImageSerializer(many=True)

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
            "brand",
            "images",
        )


class NewPopularBootsSerializer(serializers.ModelSerializer):
    images = BootsImageSerializer(many=True)

    class Meta:
        model = Boots
        fields = ("id", "name", "brand", "price", "images")
