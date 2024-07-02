from locations.models import Address, Location
from locations.serializers import LocationSerializer,AddressSerializer
from photos.serializers import ServicePhotosSerializers
from .models import FoodService,ServiceType,ServiceProviderApplication,FavoriteService,Service,DJService
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
    