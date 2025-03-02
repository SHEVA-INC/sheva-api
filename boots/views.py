from django.core.files.storage import default_storage
from django.db import transaction
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from accessories.models import Accessory
from accessories.serializers import LikedAccessorySerializer
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
        if self.action in ["retrieve", "create"]:
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


class GetItemsByIdsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IdsSerializer
    pagination_class = CustomPageNumberPagination

    MODEL_SERIALIZER_MAP = {
        'accessories': (Accessory, LikedAccessorySerializer),
        'boots': (Boots, LikedBootsSerializer),
    }

    def post(self, request):
        categories_data = request.data.get('categories', {})
        if not isinstance(categories_data, dict):
            return Response({'error': 'Invalid categories format'},
                            status=status.HTTP_400_BAD_REQUEST)

        response_data = {}
        paginator = CustomPageNumberPagination()

        all_items = []
        for category, ids in categories_data.items():
            if category not in self.MODEL_SERIALIZER_MAP:
                return Response({'error': f'Invalid category: {category}'},
                                status=status.HTTP_400_BAD_REQUEST)

            model, serializer_class = self.MODEL_SERIALIZER_MAP[category]
            items = list(model.objects.filter(id__in=ids).order_by('id'))
            items_serializer = serializer_class(items, many=True,
                                                context={'request': request})
            response_data[category] = items_serializer.data
            all_items.extend(items)

        all_items.sort(key=lambda x: x.id)
        page = paginator.paginate_queryset(all_items, request)
        if page is not None:
            paginated_response = paginator.get_paginated_response(response_data)
            return paginated_response

        return Response(response_data, status=status.HTTP_200_OK)



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
