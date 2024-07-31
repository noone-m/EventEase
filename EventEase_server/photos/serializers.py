from django.shortcuts import get_object_or_404
from .models import ServicePhotos,ServiceProfilePhoto,FoodPhotos,Food,MainFoodPhoto,DecorPhotos,MainDecorPhoto
from locations.models import Location,Address
from rest_framework import serializers

class ServicePhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServicePhotos
        fields = ['id','service','image']
        read_only_fields = ['id','service']
    

class ServiceProfilePhotoSerialzer(serializers.ModelSerializer):
    profile_photo_url = serializers.SerializerMethodField()
    class Meta:
        model = ServiceProfilePhoto
        fields = ['service', 'profile_photo_url', 'servicePhoto']
        read_only_fields = ['service']

    def get_profile_photo_url(self, obj):
        photo = obj.servicePhoto
        serializer = ServicePhotosSerializers(photo)
        return serializer.data['image']
    

class FoodPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = FoodPhotos
        fields = ['id','food','image']
        read_only_fields = ['id','food']
    

class MainFoodPhotoSerializer(serializers.ModelSerializer):
    main_photo_url = serializers.SerializerMethodField()
    class Meta:
        model = MainFoodPhoto
        fields = ['food', 'foodPhoto', 'main_photo_url']
        read_only_fields = ['food', 'main_photo_url']

    def get_main_photo_url(self, obj):
        try:
            serializer = DecorPhotosSerializer(obj['foodPhoto'])
        except TypeError:
            serializer = DecorPhotosSerializer(obj.foodPhoto)
        return serializer.data['image']
    

class DecorPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecorPhotos
        fields = ['id','decor','image']
        read_only_fields = ['id','decor']
    
class MainDecorPhotoSerializer(serializers.ModelSerializer):
    main_photo_url = serializers.SerializerMethodField()
    class Meta:
        model = MainDecorPhoto
        fields = ['decor', 'decorPhoto', 'main_photo_url']
        read_only_fields = ['decor', 'main_photo_url']

    def get_main_photo_url(self, obj):
        print(obj)
        try:
            serializer = DecorPhotosSerializer(obj['decorPhoto'])
        except TypeError:
            serializer = DecorPhotosSerializer(obj.decorPhoto)
        return serializer.data['image']