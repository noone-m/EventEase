from rest_framework import serializers
from locations.serializers import LocationSerializer
from .models import EventType,Event,InvitationCard,InvitationCardDesign

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only = True)
    event_type=EventTypeSerializer()
    class Meta:
        model = Event
        fields = ['id', 'user', 'total_cost', 'location','name', 'start_time', 'end_time', 'event_type']
        read_only_fields = ['id', 'total_cost', 'location', 'user']

class InvitationCardDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationCardDesign
        fields = '__all__'  # Include all fields in the serializer


class InvitationCardSerializer(serializers.ModelSerializer):
    design = InvitationCardDesignSerializer(read_only=True)
    event = EventSerializer(read_only = True)
    class Meta: 
        model = InvitationCard
        fields = '__all__'  # Include all fields in the serializer