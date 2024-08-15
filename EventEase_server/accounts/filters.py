from django_filters import rest_framework as filters
from .models import User


class UserFilter(filters.FilterSet):
    is_service_provider = filters.BooleanFilter()
    class Meta:
        model = User
        fields = ['is_service_provider']