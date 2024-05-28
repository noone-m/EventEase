from django.urls import path,include
from .views import (FoodServiceViewSet)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('services', FoodServiceViewSet)

urlpatterns = [
    path('',include(router.urls)),
] 