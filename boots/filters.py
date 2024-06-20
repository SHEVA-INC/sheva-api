import django_filters
from .models import Boots, Size


class BootsFilter(django_filters.FilterSet):
    size = django_filters.NumberFilter(field_name="sizes__size")
    color = django_filters.ChoiceFilter(choices=Boots.COLOR_CHOICES)
    type = django_filters.ChoiceFilter(choices=Boots.TYPE_CHOICES)

    class Meta:
        model = Boots
        fields = ['size', 'color', 'type']
