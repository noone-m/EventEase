from django_filters import rest_framework as filters
from .models import Service


class ServiceFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='location__address__country', lookup_expr='exact')
    state = filters.CharFilter(field_name='location__address__state', lookup_expr='exact')
    village_city = filters.CharFilter(field_name='location__address__village_city', lookup_expr='exact')
    street = filters.CharFilter(field_name='location__address__street', lookup_expr='exact')
    service_type = filters.CharFilter(field_name='service_type__type', lookup_expr='exact')
    class Meta:
        model = Service
        fields = ['location__address__country',
                'location__address__state',
                'location__address__village_city',
                'location__address__street',
                'service_type']

