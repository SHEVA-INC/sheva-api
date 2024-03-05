from rest_framework import viewsets

from review.models import Review
from review.permissions import IsOwnerOrReadOnly
from review.serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
