from django.core.files.storage import default_storage
from django.db import transaction
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from boots.filters import BootsFilter, CustomPageNumberPagination
from boots.models import Boots
from boots.permissions import IsAdminOrReadOnly
from boots.serializers import BootsSerializer, BootsDetailSerializer, BootsImageSerializer, \
    NewPopularBootsSerializer, LikedBootsSerializer, IdsSerializer, BootsImageUpdateSerializer, \
    MainImageUpdateSerializer, BootsUpdateSerializer


class BootsViewSet(viewsets.ModelViewSet):
    queryset = Boots.objects.all().order_by('id')
    serializer_class = BootsSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BootsFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BootsDetailSerializer
        if self.action == "create":
            return BootsDetailSerializer
        return BootsSerializer


class NewBootsList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = NewPopularBootsSerializer

    def get(self, request):
        boots = Boots.objects.filter(new=True)
        serializer = NewPopularBootsSerializer(boots, many=True, context={'request': request})
        return Response(serializer.data)


class PopularBootsList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = NewPopularBootsSerializer

    def get(self, request):
        boots = Boots.objects.filter(popular=True)
        serializer = NewPopularBootsSerializer(boots, many=True, context={'request': request})
        return Response(serializer.data)


class GetBootsByIdsView(APIView):
    queryset = Boots.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = IdsSerializer
    pagination_class = CustomPageNumberPagination

    def post(self, request):
        serializer = IdsSerializer(data=request.data)
        if serializer.is_valid():
            ids = serializer.validated_data['ids']
            boots = Boots.objects.filter(id__in=ids)

            paginator = CustomPageNumberPagination()
            page = paginator.paginate_queryset(boots, request)
            if page is not None:
                boots_serializer = LikedBootsSerializer(page, many=True, context={'request': request})
                return paginator.get_paginated_response(boots_serializer.data)

            boots_serializer = LikedBootsSerializer(boots, many=True, context={'request': request})
            return Response(boots_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BootsUpdateView(generics.UpdateAPIView):
    queryset = Boots.objects.all()
    serializer_class = BootsUpdateSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        return Boots.objects.get(id=self.kwargs['pk'])


class MainImageUpdateView(generics.UpdateAPIView):
    queryset = Boots.objects.all()
    serializer_class = MainImageUpdateSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        return Boots.objects.get(id=self.kwargs['pk'])


class BootsImagesUpdateView(generics.UpdateAPIView):
    queryset = Boots.objects.all()
    serializer_class = BootsImageUpdateSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        return Boots.objects.get(id=self.kwargs['pk'])

    # def post(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     with transaction.atomic():
    #         self.perform_update(serializer)
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def perform_update(self, serializer):
    #     serializer.save()
