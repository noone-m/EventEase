from django.urls import path,include
from .views import (FoodServiceViewSet,ServiceTypeViewSet,ServiceProviderApplicationView,ApproveApplication,
ServiceViewSet,DeclineApplication,ServiceProviderApplicationDetailView)
from photos.views import ServicePhotosAPIView,ServiceProfilePhotoAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register('food-services', FoodServiceViewSet)
router.register('type',ServiceTypeViewSet)
router.register('',ServiceViewSet)

# router.register('locations',LocationViewSet)
urlpatterns = [
    path('applications/',ServiceProviderApplicationView.as_view()),
    path('applications/<int:pk>/',ServiceProviderApplicationDetailView.as_view()),
    path('applications/<int:pk>/approve/',ApproveApplication.as_view()),
    path('applications/<int:pk>/decline/',DeclineApplication.as_view()),
    path('<int:service_pk>/photos/',ServicePhotosAPIView.as_view()),
    path('<int:service_pk>/photos/<int:photo_pk>/',ServicePhotosAPIView.as_view()),
    path('<int:service_pk>/profile-photo/',ServiceProfilePhotoAPIView.as_view()),
    path('',include(router.urls)),
] 
