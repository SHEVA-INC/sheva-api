from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from boots.models import Boots
from boots.serializers import BootsSerializer, BootsDetailSerializer, BootsImageSerializer, \
    NewPopularBootsSerializer


class BootsViewSet(viewsets.ModelViewSet):
    queryset = Boots.objects.all()
    serializer_class = BootsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BootsDetailSerializer

        return BootsSerializer


class NewBootsList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        boots = Boots.objects.filter(new=True)
        serializer = NewPopularBootsSerializer(boots, many=True)
        return Response(serializer.data)

class PopularBootsList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        boots = Boots.objects.filter(popular=True)
        serializer = NewPopularBootsSerializer(boots, many=True)
        return Response(serializer.data)
