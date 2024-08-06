from django_filters import rest_framework as filters
from .models import Service

class ServiceFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='location__address__country', lookup_expr='icontains')
    state = filters.CharFilter(field_name='location__address__state', lookup_expr='icontains')
    village_city = filters.CharFilter(field_name='location__address__village_city', lookup_expr='icontains')
    street = filters.CharFilter(field_name='location__address__street', lookup_expr='icontains')

    class Meta:
        model = Service
        fields = ['country', 'state', 'village_city', 'street']
