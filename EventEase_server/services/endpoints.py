from django.urls import path,include
from .views import (FoodServiceViewSet,ServiceTypeViewSet,ServiceProviderApplicationView,ApproveApplication,
ServiceViewSet,DeclineApplication,ServiceProviderApplicationDetailView,FoodTypeAPIView,
DeleteRetrieveFoodTypeAPIView,FoodAPIView,LocationDetailView)
from photos.views import ServicePhotosAPIView,ServiceProfilePhotoAPIView,FoodPhotosAPIView,MainFoodPhotoAPIView
from locations.views import AddressViewSet,LocationViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register('food-services', FoodServiceViewSet)
router.register(r'locations', LocationViewSet)
router.register('type',ServiceTypeViewSet)
router.register(r'addresses', AddressViewSet)   
router.register('',ServiceViewSet)


# router.register('locations',LocationViewSet)
urlpatterns = [
    path('applications/',ServiceProviderApplicationView.as_view()),
    path('applications/<int:pk>/',ServiceProviderApplicationDetailView.as_view()),
    path('applications/<int:pk>/approve/',ApproveApplication.as_view()),
    path('applications/<int:pk>/decline/',DeclineApplication.as_view()),
    path('<int:service_pk>/photos/',ServicePhotosAPIView.as_view()),
    path('<int:service_pk>/location/',LocationDetailView.as_view()),
    path('<int:service_pk>/photos/<int:photo_pk>/',ServicePhotosAPIView.as_view()),
    path('<int:service_pk>/profile-photo/',ServiceProfilePhotoAPIView.as_view()),
    path('<int:service_pk>/food-type/',FoodTypeAPIView.as_view()),
    path('<int:service_pk>/food-type/<int:type_pk>/',DeleteRetrieveFoodTypeAPIView.as_view()),
    path('<int:service_pk>/food-type/<int:type_pk>/food/', FoodAPIView.as_view(), name='food-list-create'),
    path('<int:service_pk>/food-type/<int:type_pk>/food/<int:food_pk>/', FoodAPIView.as_view(), name='food-list-create'),
    path('<int:service_pk>/food-type/<int:type_pk>/food/<int:food_pk>/photos/', FoodPhotosAPIView.as_view(), name='food-list-create'),
    path('<int:service_pk>/food-type/<int:type_pk>/food/<int:food_pk>/photos/<int:photo_pk>/', FoodPhotosAPIView.as_view()),
    path('<int:service_pk>/food-type/<int:type_pk>/food/<int:food_pk>/photos/main/', MainFoodPhotoAPIView.as_view()),
    path('',include(router.urls)),
] 
