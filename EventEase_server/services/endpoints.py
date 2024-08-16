from django.urls import path,include
from .views import (FoodServiceViewSet,ServiceTypeViewSet,ServiceProviderApplicationView,ApproveApplication,
ServiceViewSet,DeclineApplication,ServiceProviderApplicationDetailView,FoodTypeAPIView,
DeleteRetrieveFoodTypeAPIView,FoodAPIView,LocationDetailView,DecorAPIView,MyServiceAPIView,
MyServiceTypeAPIView, ServiceReservationAPIView,RejectServiceReservationAPIView,ListRetrieveFoodAPIView,
ConfirmServiceReservationAPIView, CancelServiceReservation, ServicesReservationsAPIView, 
DecorsReservationsAPIView, DecorsReservationAPIView, ConfirmDecorsServiceReservationAPIView,
RejectDecorsServiceReservationAPIView, CancelDecorsServiceReservation, FoodOrderAPIView, RejectFoodOrderAPIView,
ConfirmFoodOrderAPIView, ListOrdersAPIview, CancelFoodOrder, PayFoodOrder, PayDecorsServiceReservation,
PayServiceReservation,)

from photos.views import (ServicePhotosAPIView,ServiceProfilePhotoAPIView,FoodPhotosAPIView,MainFoodPhotoAPIView
,DecorPhotosAPIView,MainDecorPhotoAPIView)

from locations.views import AddressViewSet,LocationViewSet

from reports.views import (ReportReviewAPIView,SolveReportReviewAPIView,ReportServiceAPIView,SolveReportServiceAPIView,
ListAllReviewsReports, ListAllServicesReports)
from videos.views import VideoListCreateAPIView,VideoRetrieveDestroyAPIView

from reviews.views import ReviewListCreateAPIView,ReviewUpdateDestroyAPIView
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

    path('my-service/',MyServiceAPIView.as_view()),
    path('my-service/type',MyServiceTypeAPIView.as_view()),
    path('services-reservations/',ServicesReservationsAPIView.as_view()),
    path('decors-reservations/',DecorsReservationsAPIView.as_view()),
    path('food-orders/',ListOrdersAPIview.as_view()),

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
    path('<int:service_pk>/food/',ListRetrieveFoodAPIView.as_view()),
    path('<int:service_pk>/food/<int:food_pk>/',ListRetrieveFoodAPIView.as_view()),


    path('<int:service_pk>/decors/', DecorAPIView.as_view()),
    path('<int:service_pk>/decors/<int:decor_pk>/', DecorAPIView.as_view()),
    path('<int:service_pk>/decors/<int:decor_pk>/photos/', DecorPhotosAPIView.as_view(), name='food-list-create'),
    path('<int:service_pk>/decors/<int:decor_pk>/photos/<int:photo_pk>/', DecorPhotosAPIView.as_view()),
    path('<int:service_pk>/decors/<int:decor_pk>/photos/main/', MainDecorPhotoAPIView.as_view()),

    path('<int:service_pk>/reviews/', ReviewListCreateAPIView.as_view()),
    path('<int:service_pk>/reviews/<int:review_pk>/', ReviewUpdateDestroyAPIView.as_view()),
    path('<int:service_pk>/reviews/<int:review_pk>/reports/', ReportReviewAPIView.as_view()),
    path('<int:service_pk>/reviews/<int:review_pk>/reports/<int:report_pk>/', ReportReviewAPIView.as_view()),
    path('<int:service_pk>/reviews/<int:review_pk>/reports/<int:report_pk>/solve/',SolveReportReviewAPIView.as_view()),
    
    path('<int:service_pk>/reports/', ReportServiceAPIView.as_view()),
    path('<int:service_pk>/reports/<int:report_pk>/', ReportServiceAPIView.as_view()),
    path('<int:service_pk>/reports/<int:report_pk>/solve/',SolveReportServiceAPIView.as_view()),

    path('reviews-reports/', ListAllReviewsReports.as_view()),
    path('services-reports/', ListAllServicesReports.as_view()),

    path('<int:service_pk>/videos/',VideoListCreateAPIView.as_view()),   
    path('<int:service_pk>/videos/<int:video_pk>/',VideoRetrieveDestroyAPIView.as_view()), 

    path('<int:service_pk>/reservations/',ServiceReservationAPIView.as_view()), 
    path('<int:service_pk>/reservations/<int:reservation_pk>/',ServiceReservationAPIView.as_view()), 
    path('<int:service_pk>/reservations/<int:reservation_pk>/reject/',RejectServiceReservationAPIView.as_view()), 
    path('<int:service_pk>/reservations/<int:reservation_pk>/confirm/',ConfirmServiceReservationAPIView.as_view()),
    path('<int:service_pk>/reservations/<int:reservation_pk>/cancel/',CancelServiceReservation.as_view()), 
    path('<int:service_pk>/reservations/<int:reservation_pk>/pay/',PayServiceReservation.as_view()),

    path('<int:service_pk>/decors-reservations/', DecorsReservationAPIView.as_view()),
    path('<int:service_pk>/decors-reservations/<int:reservation_pk>/reject/', RejectDecorsServiceReservationAPIView.as_view()),
    path('<int:service_pk>/decors-reservations/<int:reservation_pk>/confirm/', ConfirmDecorsServiceReservationAPIView.as_view()), 
    path('<int:service_pk>/decors-reservations/<int:reservation_pk>/cancel/', CancelDecorsServiceReservation.as_view()), 
    path('<int:service_pk>/decors-reservations/<int:reservation_pk>/pay/', PayDecorsServiceReservation.as_view()),

    path('<int:service_pk>/food-order/',FoodOrderAPIView.as_view()),
    path('<int:service_pk>/food-order/<int:order_pk>/reject/', RejectFoodOrderAPIView.as_view()),
    path('<int:service_pk>/food-order/<int:order_pk>/confirm/', ConfirmFoodOrderAPIView.as_view()),
    path('<int:service_pk>/food-order/<int:order_pk>/cancel/', CancelFoodOrder.as_view()),
    path('<int:service_pk>/food-order/<int:order_pk>/pay/', PayFoodOrder.as_view()),

    path('',include(router.urls)),
] 
