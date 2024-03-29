from rest_framework import serializers
from .models import Review, Boots
from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    boots_name = serializers.CharField(source='boots.name', read_only=True)
    boots = serializers.PrimaryKeyRelatedField(queryset=Boots.objects.all(), write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'boots', 'boots_name', 'username', 'text', 'rating', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance
