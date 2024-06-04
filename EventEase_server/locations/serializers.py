from rest_framework import serializers
from .models import Address, Location

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only = True)
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['address']
