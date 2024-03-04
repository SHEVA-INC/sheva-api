from rest_framework import viewsets

from boots.models import Boots
from boots.serializers import BootsSerializer


class BootsViewSet(viewsets.ModelViewSet):
    queryset = Boots.objects.all()
    serializer_class = BootsSerializer
