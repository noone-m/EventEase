from .models import ServicePhotos,ServiceProfilePhoto,FoodPhotos,Food,MainFoodPhoto
from rest_framework import serializers

class ServicePhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServicePhotos
        fields = ['id','service','image']
        read_only_fields = ['id','service']
    

class ServiceProfilePhotoSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProfilePhoto
        fields = '__all__'
        read_only_fields = ['id','service']


class FoodPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = FoodPhotos
        fields = ['id','food','image']
        read_only_fields = ['id','food']
    

class MainFoodPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainFoodPhoto
        fields = ['id', 'food', 'foodPhoto']
        read_only_fields = ['id', 'food']