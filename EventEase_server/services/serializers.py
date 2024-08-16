from locations.models import Address, Location
from events.models import EventType
from locations.serializers import LocationSerializer,AddressSerializer
from events.serializers import EventTypeSerializer
from accounts.serializers import AdminUserSerializer
from photos.serializers import ServicePhotosSerializers
from .models import (FoodService, ServiceReservation, ServiceType, ServiceProviderApplication, FavoriteService, Service, DJService, Food
, FoodType, FoodTypeService, FoodServiceFood, Venue, PhotoGrapherService, EntertainementService, Decor,
DecorEventType,DecorationService, DecorsReservation, Reservation,Order,FoodInOrder)
from rest_framework import serializers


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class FoodServiceSerializer(serializers.ModelSerializer):
    service_provider = AdminUserSerializer(read_only=True)
    service_type = ServiceTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    class Meta:
        model = FoodService
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
    service_provider = AdminUserSerializer(read_only=True)
    service_type = ServiceTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    class Meta:
        model = Service
        fields = '__all__'


class DJServiceSerializer(serializers.ModelSerializer):
    service_provider = AdminUserSerializer(read_only=True)
    service_type = ServiceTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    class Meta:
        model = DJService
        fields = '__all__'
    
class FoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodType
        fields = '__all__'


class FoodTypeServiceSerializer(serializers.ModelSerializer):
    foodType = FoodTypeSerializer(read_only =True)
    class Meta:
        model = FoodTypeService
        fields = ['foodType','foodService']


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'food_type', 'name', 'price', 'ingredients']
        read_only_fields = ['id','food_type']

class FoodServiceFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer()

    class Meta:
        model = FoodServiceFood
        fields = ['foodService', 'food']

class VenueSerializer(serializers.ModelSerializer):
    service_provider = AdminUserSerializer(read_only=True)
    service_type = ServiceTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
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
    service_provider = AdminUserSerializer(read_only=True)
    service_type = ServiceTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    class Meta:
        model = EntertainementService
        fields = '__all__'

class DecorationServiceSerializer(serializers.ModelSerializer):
    service_provider = AdminUserSerializer(read_only=True)
    service_type = ServiceTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    class Meta:
        model = DecorationService
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
        read_only_fields = ['id','available_quantity','decor_service']

    def get_decor_event_types(self, obj):
        print(obj)
        decor_event_types = DecorEventType.objects.filter(decor=obj)
        print(decor_event_types)
        return DecorEventTypeSerializer(decor_event_types, many=True).data
    

class MyServiceTypeSerializer(serializers.Serializer):
    service_id = serializers.IntegerField(read_only = True)
    type_id = serializers.IntegerField(read_only = True)
    type = serializers.StringRelatedField(read_only = True)
    avg_rating = serializers.FloatField(read_only = True)


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Reservation
        fields = ['event', 'start_time', 'end_time', 'status', 'cost', 'created_at']
        read_only_fields = ['event', 'start_time', 'end_time', 'status', 'cost', 'created_at']


class ServiceReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReservation
        fields = '__all__'
        read_only_fields = ['id', 'service', 'cost', 'status']


class DecorsReservationSerializer(serializers.ModelSerializer):
    class Meta:
        # decors = 
        model = DecorsReservation
        fields = '__all__'
        read_only_fields = ['id', 'decor_service', 'cost', 'status']


class NewFoodTypeSerializer(serializers.Serializer):
    new_type = serializers.IntegerField()

class DecorsQuantitySerializer(serializers.Serializer):
    decor_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class DecorsListSerializer(serializers.Serializer):
    decors = serializers.ListField(child=DecorsQuantitySerializer())


class OrderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'service', 'status', 'total_price', 'created_at']

class FoodsQuantitySerializer(serializers.Serializer):
    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class FoodsListSerializer(serializers.Serializer):
    foods = serializers.ListField(child=FoodsQuantitySerializer())