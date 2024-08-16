from django.shortcuts import get_object_or_404
import requests
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from locations.models import Address, Location
from locations.utils import get_location_from_osm
from locations.serializers import LocationSerializer
from .models import EventType,Event,InvitationCardDesign,InvitationCard
from .serializers import EventTypeSerializer, EventSerializer,InvitationCardDesignSerializer, InvitationCardSerializer
from accounts.permissions import IsAdminUser,IsAuthenticated, IsOwner, IsOwnerOrAdminUser,Default

class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy','creat']:
            return [IsAdminUser()]
        elif self.action in['list','retrieve']:
            return [IsAuthenticated()]
        else:
            pass
        return super().get_permissions()
    

class EventAPIView(APIView):

    def get(self,request,event_id=None):
        if event_id:
            event = get_object_or_404(Event,pk = event_id)
            serializer = EventSerializer(event)
            return Response(serializer.data,status= status.HTTP_200_OK)
        else:
            if request.user.is_superuser:
                events = Event.objects.all()
            else:
                events = Event.objects.filter(user = request.user)
            serializer = EventSerializer(events, many = True)
            return Response(serializer.data,status= status.HTTP_200_OK)
        
    def post(self,request, event_id = None):
        event_serializer = EventSerializer(data = request.data)
        location_serializer = LocationSerializer(data = request.data)
        if location_serializer.is_valid():
            latitude = location_serializer.validated_data['latitude']
            longitude = location_serializer.validated_data['longitude']
            location = get_location_from_osm(latitude, longitude)
            if event_serializer.is_valid():
                event_serializer.save(user = request.user,location = location)
                return Response(event_serializer.data,status= status.HTTP_201_CREATED)
            return Response(event_serializer.errors,status= status.HTTP_400_BAD_REQUEST)
        return Response(location_serializer.errors,status= status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,event_id=None):
        event = get_object_or_404(Event,id = event_id)
        event_serializer = EventSerializer(event, data = request.data, partial = True)
        location_serializer = LocationSerializer(data = request.data)
        if location_serializer.is_valid():
            latitude = location_serializer.validated_data['latitude']
            longitude = location_serializer.validated_data['longitude']
            location = get_location_from_osm(latitude, longitude)
            if event_serializer.is_valid():
                event_serializer.save(location = location)
                return Response(event_serializer.data,status= status.HTTP_201_CREATED)
            return Response(event_serializer.errors,status= status.HTTP_400_BAD_REQUEST)
        else:
            if event_serializer.is_valid():
                event_serializer.save()
                return Response(event_serializer.data,status= status.HTTP_201_CREATED)
            return Response(event_serializer.errors,status= status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,event_id=None):
        event = get_object_or_404(Event,id = event_id)
        event.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsOwner()]
        if self.request.method in ['DELETE','GET']:
            return [IsOwnerOrAdminUser()]
        if self.request.method == 'POST':
            return  [Default()]
    


class InvitationCardDesignListCreateAPIView(APIView):
    def get(self, request):
        designs = InvitationCardDesign.objects.all()
        serializer = InvitationCardDesignSerializer(designs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InvitationCardDesignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvitationCardDesignDetailAPIView(APIView):
    def get(self, request, pk):
        design = get_object_or_404(InvitationCardDesign, pk=pk)
        serializer = InvitationCardDesignSerializer(design)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        design = get_object_or_404(InvitationCardDesign, pk=pk)
        serializer = InvitationCardDesignSerializer(design, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        design = get_object_or_404(InvitationCardDesign, pk=pk)
        design.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class InvitationCardListCreateAPIView(APIView):
    def get(self, request):
        cards = InvitationCard.objects.all()
        serializer = InvitationCardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InvitationCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class InvitationCardDetailAPIView(APIView):
    def get(self, request, pk):
        card = get_object_or_404(InvitationCard, pk=pk)
        serializer = InvitationCardSerializer(card)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        card = get_object_or_404(InvitationCard, pk=pk)
        serializer = InvitationCardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        card = get_object_or_404(InvitationCard, pk=pk)
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
