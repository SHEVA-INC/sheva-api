import django_filters

from accessories.models import Accessory


class AccessoriesFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(choices=Accessory.TYPE_CHOICES)

    class Meta:
        model = Accessory
        fields = ['type']

