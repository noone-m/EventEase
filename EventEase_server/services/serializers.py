from locations.models import Address, Location
from events.models import EventType
from locations.serializers import LocationSerializer,AddressSerializer
from events.serializers import EventTypeSerializer
from photos.serializers import ServicePhotosSerializers
from .models import (FoodService, ServiceType, ServiceProviderApplication, FavoriteService, Service, DJService, Food
, FoodType, FoodTypeService, FoodServiceFood, Venue, PhotoGrapherService, EntertainementService, Decor,
DecorEventType)
from rest_framework import serializers

class FoodServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodService
        fields = '__all__'
    

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class ServiceProviderApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceProviderApplication
        fields = '__all__'
        read_only_fields = ['id','user','location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and not request.user.is_superuser:
            self.fields['status'].read_only = True  # Make status read-only for non-superusers
        if request and request.method == 'GET':
            print('true')
            self.fields['service_type'] = ServiceTypeSerializer(read_only = True)
            self.fields['location'] = LocationSerializer(read_only =True)
    
    def validate(self, attrs):
        print(attrs)
        request = self.context['request']
        if request.method == 'PUT':
            if ('service_type' in attrs and 'other_type' in attrs):
                raise serializers.ValidationError("Request body should contain either 'service_type' or 'other_type', not both.")
        elif ('service_type' in attrs and 'other_type' in attrs) or ('service_type' not in attrs and 'other_type' not in attrs):
            raise serializers.ValidationError("Request body should contain either 'service_type' or 'other_type', not both.")
        return super().validate(attrs)

class FavoriteServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteService
        fields = '__all__'
        read_only_fields = ['id','user']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class DJServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DJService
        fields = '__all__'
    
class FoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodType
        fields = '__all__'


class FoodTypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTypeService
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'food_type', 'name', 'price', 'ingredients']

class FoodServiceFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer()

    class Meta:
        model = FoodServiceFood
        fields = ['id', 'foodService', 'food']

class VenueSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method in ['PUT','PATCH']:
            self.fields['location'].read_only = True
    
    class Meta:
        model = Venue
        fields = '__all__'
    

class PhotoGrapherServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoGrapherService
        fields = '__all__'

class EntertainementServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntertainementService
        fields = '__all__'

class DecorationServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntertainementService
        fields = '__all__'

class DecorEventTypeSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer()
    class Meta:
        model = DecorEventType
        fields = ['event_type']
    
class DecorEventTypeListSerializer(serializers.Serializer):
    decor_event_types = serializers.ListField()

class DecorSerializer(serializers.ModelSerializer):
    decor_event_types = serializers.SerializerMethodField()
    class Meta:
        model = Decor
        fields = ['id','decor_service', 'name', 'quantity', 'hourly_rate', 'available_quantity', 'price', 'description','decor_event_types']
        read_only_fields = ['id','avialable_quantity','decor_service','available_quantity']

    def get_decor_event_types(self, obj):
        print(obj)
        decor_event_types = DecorEventType.objects.filter(decor=obj)
        print(decor_event_types)
        return DecorEventTypeSerializer(decor_event_types, many=True).data
    

