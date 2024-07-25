from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EventTypeViewSet

router = DefaultRouter()
router.register('types', EventTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
