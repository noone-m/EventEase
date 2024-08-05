from rest_framework import serializers
from locations.serializers import LocationSerializer
from .models import EventType,Event

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only = True)
    class Meta:
        model = Event
        fields = ['id', 'user', 'total_cost', 'location','name', 'start_time', 'end_time']
        read_only_fields = ['id', 'total_cost', 'location', 'user']