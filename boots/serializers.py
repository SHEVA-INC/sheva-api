from rest_framework import serializers
from boots.models import Boots, BootsImage, Size


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('size',)


class BootsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BootsImage
        fields = ("image",)

class BootsSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    images = BootsImageSerializer(many=True)
    uploaded_images = serializers.ListField(child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True)

    class Meta:
        model = Boots
        fields = (
            "id",
            "name",
            "price",
            "color",
            "brand",
            "sizes",
            "images",
            "uploaded_images",
            "main_image",
        )

    def create(self, validated_data):
        sizes_data = validated_data.pop('sizes')
        uploaded_images = validated_data.pop("uploaded_images")
        boots = Boots.objects.create(**validated_data)
        for size_data in sizes_data:
            Size.objects.create(boots=boots, **size_data)
        for image in uploaded_images:
            BootsImage.objects.create(boots=boots, image=image)

        return boots

class BootsDetailSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    images = BootsImageSerializer(many=True)

    class Meta:
        model = Boots
        fields = (
            "id",
            "name",
            "description",
            "price",
            "color",
            "sizes",
            "brand",
            "images",
            "main_image",
        )


class NewPopularBootsSerializer(serializers.ModelSerializer):
    images = BootsImageSerializer(many=True)

    class Meta:
        model = Boots
        fields = ("id", "name", "brand", "price", "images")


class BootsCartSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True)

    class Meta:
        model = Boots
        fields = ("name", "brand", "price", "color", "main_image", "uploaded_images")
