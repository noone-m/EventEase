from .models import ServicePhotos,ServiceProfilePhoto,FoodPhotos,Food,MainFoodPhoto,DecorPhotos,MainDecorPhoto
from locations.models import Location,Address
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


class DecorPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecorPhotos
        fields = ['id','decor','image']
        read_only_fields = ['id','decor']
    
class MainDecorPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainDecorPhoto
        fields = ['id', 'decor', 'decorPhoto']
        read_only_fields = ['id', 'decor']