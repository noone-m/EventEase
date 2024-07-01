from django.urls import path,include
from .views import (FoodServiceViewSet,ServiceTypeViewSet,ServiceProviderApplicationView,ApproveApplication,
ServiceViewSet)
from photos.views import ServicePhotosAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register('food-services', FoodServiceViewSet)
router.register('type',ServiceTypeViewSet)
router.register('',ServiceViewSet)

# router.register('locations',LocationViewSet)
urlpatterns = [
    path('',include(router.urls)),
    path('applications/',ServiceProviderApplicationView.as_view()),
    path('applications/<int:pk>/approve/',ApproveApplication.as_view()),
    path('<int:pk>/photos/',ServicePhotosAPIView.as_view()),
] 
