from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from accounts.permissions import IsOwnerOrAdminUser
from .models import Review, Service
from .serializers import ReviewSerializer

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        service_id = self.kwargs['service_pk']
        return Review.objects.filter(service_id=service_id)

    def perform_create(self, serializer):
        service_id = self.kwargs['service_pk']
        service = Service.objects.get(pk=service_id)
        try:
            serializer.save(user=self.request.user, service=service)
        except IntegrityError:
            raise ValidationError({'message':'You have already reviewed this service.'})
        

class ReviewUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdminUser]
    lookup_url_kwarg = 'review_pk'

    def get_queryset(self):
        service_id = self.kwargs['service_pk']
        return Review.objects.filter(service_id=service_id)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise ValidationError('You are not allowed to edit this review.')
        serializer.save()
