from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from accessories.filters import AccessoriesFilter
from accessories.models import Accessory
from accessories.serializers import AccessoriesListSerializer, AccessoriesSerializer
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
