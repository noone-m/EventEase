from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import AddressSerializer,LocationSerializer
from .models import Address,Location
from accounts.permissions import IsAuthenticated,IsAdminUser

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
    permission_classes = [IsAdminUser]
