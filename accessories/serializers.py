from urllib.parse import urljoin

from rest_framework import serializers

from accessories.models import Accessory


def build_absolute_uri(request, relative_url):
    return urljoin(request.build_absolute_uri('/'), relative_url)


class AccessoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = '__all__'


class AccessoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = ["id", "name", "price", "main_image", "type", "size"]


class IdsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=True)


class LikedAccessorySerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Accessory
        fields = (
        "id", "name", "type", "price", "main_image", "size", "description")

    def get_main_image(self, obj):
        request = self.context.get('request')
        return build_absolute_uri(request, obj.main_image.url)
