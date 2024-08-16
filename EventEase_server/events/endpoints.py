from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (EventTypeViewSet,EventAPIView,InvitationCardDesignDetailAPIView,InvitationCardDesignListCreateAPIView,
InvitationCardDetailAPIView,InvitationCardListCreateAPIView)

router = DefaultRouter()
router.register('types', EventTypeViewSet)

urlpatterns = [
    path('',EventAPIView.as_view()),
    path('<int:event_id>/',EventAPIView.as_view()),
    path('invitation-card-designs/', InvitationCardDesignListCreateAPIView.as_view(), name='invitation_card_design_list_create'),
    path('invitation-card-designs/<int:pk>/', InvitationCardDesignDetailAPIView.as_view(), name='invitation_card_design_detail'),
    path('invitation_cards/', InvitationCardListCreateAPIView.as_view(), name='invitation_card_list_create'),
    path('invitation_cards/<int:pk>/', InvitationCardDetailAPIView.as_view(), name='invitation_card_detail'),
    path('', include(router.urls)),
]
