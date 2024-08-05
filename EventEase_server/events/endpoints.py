from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EventTypeViewSet,EventAPIView

router = DefaultRouter()
router.register('types', EventTypeViewSet)

urlpatterns = [
    path('',EventAPIView.as_view()),
    path('<int:event_id>/',EventAPIView.as_view()),
    path('', include(router.urls)),
]
