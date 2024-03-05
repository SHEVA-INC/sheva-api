from rest_framework import viewsets

from boots.models import Boots
from boots.serializers import BootsSerializer, BootsDetailSerializer,  BootsImageSerializer


class BootsViewSet(viewsets.ModelViewSet):
    queryset = Boots.objects.all()
    serializer_class = BootsSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BootsDetailSerializer

        return BootsSerializer
