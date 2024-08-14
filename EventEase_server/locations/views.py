from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from .serializers import AddressSerializer,LocationSerializer
from .models import Address,Location
from accounts.permissions import IsAuthenticated,IsAdminUser,DefaultOrIsAdminUser
from django_filters.rest_framework import DjangoFilterBackend


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            self.permission_classes = [IsAdminUser]
        elif self.action in['list','retrieve']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [DefaultOrIsAdminUser]
    search_fields = ['address__country','address__state','address__street','address__village_city']
    filter_backends = (SearchFilter,)