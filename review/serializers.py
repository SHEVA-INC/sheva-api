from rest_framework import serializers
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "boots",
            "user",
            "text",
            "rating",
            "created_at",
        )