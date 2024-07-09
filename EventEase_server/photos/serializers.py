from .models import ServicePhotos,ServiceProfilePhoto
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