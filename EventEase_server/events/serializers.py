from rest_framework import serializers
from locations.serializers import LocationSerializer
from .models import EventType,Event,InvitationCard,InvitationCardDesign

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only = True)
    event_type = serializers.PrimaryKeyRelatedField(queryset=EventType.objects.all())
    event_type_details = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['id', 'user', 'total_cost', 'location','name', 'start_time', 'end_time', 'event_type','event_type_details']
        read_only_fields = ['id', 'total_cost', 'location', 'user','event_type_details']
    
    def get_event_type_details(self, obj):
        # This method returns the serialized event_type when reading
        return EventTypeSerializer(obj.event_type).data

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