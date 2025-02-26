from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accessories.filters import AccessoriesFilter
from accessories.models import Accessory
from accessories.serializers import AccessoriesListSerializer, \
    AccessoriesSerializer, IdsSerializer, LikedAccessorySerializer
from boots.filters import CustomPageNumberPagination
from boots.permissions import IsAdminOrReadOnly


class AccessoriesViewSet(viewsets.ModelViewSet):
    queryset = Accessory.objects.all().order_by('id')
    serializer_class = AccessoriesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccessoriesFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ["retrieve", "create"]:
            return AccessoriesSerializer
        return AccessoriesListSerializer


class GetAccessoriesByIdsView(APIView):
    queryset = Accessory.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = IdsSerializer
    pagination_class = CustomPageNumberPagination

    def post(self, request):
        serializer = IdsSerializer(data=request.data)
        if serializer.is_valid():
            ids = serializer.validated_data['ids']
            accessories = Accessory.objects.filter(id__in=ids)

            paginator = CustomPageNumberPagination()
            page = paginator.paginate_queryset(accessories, request)
            if page is not None:
                accessories_serializer = LikedAccessorySerializer(page, many=True, context={'request': request})
                return paginator.get_paginated_response(accessories_serializer.data)

            accessories_serializer = LikedAccessorySerializer(accessories, many=True, context={'request': request})
            return Response(accessories_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
