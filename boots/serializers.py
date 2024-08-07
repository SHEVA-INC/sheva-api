import json

from rest_framework import serializers
from boots.models import Boots, BootsImage, Size
from urllib.parse import urljoin


def build_absolute_uri(request, relative_url):
    return urljoin(request.build_absolute_uri('/'), relative_url)


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('size', 'stock')


class BootsImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BootsImage
        fields = ("image_url",)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return build_absolute_uri(request, obj.image.url)


class BootsSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    uploaded_images = BootsImageSerializer(source='images', many=True)

    class Meta:
        model = Boots
        fields = (
            "id",
            "name",
            "price",
            "color",
            "brand",
            "sizes",
            "uploaded_images",
            "main_image",
            "type"
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

    def update(self, instance, validated_data):
        sizes_data = validated_data.pop('sizes', None)
        uploaded_images = validated_data.pop("uploaded_images", None)

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.color = validated_data.get('color', instance.color)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.main_image = validated_data.get('main_image', instance.main_image)
        instance.save()

        # Оновлення розмірів
        if sizes_data:
            instance.sizes.all().delete()
            for size_data in sizes_data:
                Size.objects.create(boots=instance, **size_data)

        # Оновлення зображень
        if uploaded_images:
            instance.images.all().delete()
            for image in uploaded_images:
                BootsImage.objects.create(boots=instance, image=image)

        return instance


class BootsDetailSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    images = BootsImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(use_url=True),
        write_only=True
    )

    class Meta:
        model = Boots
        fields = (
            "id",
            "name",
            "description",
            "price",
            "color",
            "new",
            "popular",
            "sizes",
            "brand",
            "images",
            "uploaded_images",
            "main_image",
            "type"
        )

    def create(self, validated_data):
        sizes_data = validated_data.pop('sizes', [])
        uploaded_images = validated_data.pop('uploaded_images', [])
        boots = super().create(validated_data)
        for image in uploaded_images:
            BootsImage.objects.create(boots=boots, image=image)
        print(sizes_data)
        for size_data in sizes_data:
            Size.objects.create(boots=boots, **size_data)
        return boots


class NewPopularBootsSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Boots
        fields = ("id", "name", "brand", "price", "main_image")

    def get_main_image(self, obj):
        request = self.context.get('request')
        return build_absolute_uri(request, obj.main_image.url)


class BootsCartSerializer(serializers.ModelSerializer):
    uploaded_images = BootsImageSerializer(source='images', many=True)

    class Meta:
        model = Boots
        fields = (
            "id",
            "name",
            "price",
            "color",
            "brand",
            "uploaded_images",
            "main_image",
            "type"
        )

class LikedBootsSerializer(serializers.ModelSerializer):
    uploaded_images = BootsImageSerializer(source='images', many=True)
    sizes = SizeSerializer(many=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Boots
        fields = ("id", "name", "type", "brand", "price", "main_image", "color", "uploaded_images", "sizes")

    def get_main_image(self, obj):
        request = self.context.get('request')
        return build_absolute_uri(request, obj.main_image.url)


class IdsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=True)


class BootsUpdateSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True, required=False)

    class Meta:
        model = Boots
        fields = (
        "name", "description", "price", "color", "brand", "type", "new", "popular", "sizes")

    def update(self, instance, validated_data):
        sizes_data = validated_data.pop('sizes', [])

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.color = validated_data.get('color', instance.color)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.type = validated_data.get('type', instance.type)
        instance.new = validated_data.get('new', instance.new)
        instance.popular = validated_data.get('popular', instance.popular)
        instance.save()

        instance.sizes.all().delete()

        for size_data in sizes_data:
            Size.objects.create(boots=instance, **size_data)

        return instance


class MainImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boots
        fields = ("main_image",)


# class BootsImageUpdateSerializer(serializers.Serializer):
#     images = serializers.ListField(
#         child=serializers.ImageField(),
#         write_only=True
#     )
#
#     def update(self, instance, validated_data):
#         images_data = validated_data.pop('images', [])
#         for image_data in images_data:
#             BootsImage.objects.create(boots=instance, image=image_data)
#         return instance


class BootsImageUpdateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=True, use_url=True),
        write_only=True
    )

    class Meta:
        model = Boots
        fields = ("uploaded_images",)

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')

        for old_image in instance.images.all():
            old_image.delete()

        for image_data in uploaded_images:
            BootsImage.objects.create(boots=instance, image=image_data)

        return instance



