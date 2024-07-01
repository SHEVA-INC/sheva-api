import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Boots, Size


class BootsFilter(django_filters.FilterSet):
    size = django_filters.NumberFilter(field_name="sizes__size")
    color = django_filters.ChoiceFilter(choices=Boots.COLOR_CHOICES)
    type = django_filters.ChoiceFilter(choices=Boots.TYPE_CHOICES)

    class Meta:
        model = Boots
        fields = ['size', 'color', 'type']


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
