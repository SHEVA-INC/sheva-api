from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from review.models import Review
from review.serializers import ReviewSerializer


class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Відгук надіслано!"}, status=status.HTTP_201_CREATED)


class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response({"error": "Ви не можете видалити цей відгук"}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)


class DeleteReviewView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return Response({'message': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)