from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from accounts.permissions import IsAdminUser,IsOwner
from .models import FoodService
from .serializers import FoodServiceSerializer

class FoodServiceViewSet(ModelViewSet):
    queryset = FoodService.objects.all()
    serializer_class = FoodServiceSerializer
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser|IsOwner]
        elif self.action in['list','create']:
            self.permission_classes = [IsAdminUser]
        else:
            pass
        return super().get_permissions()
