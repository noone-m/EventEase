from .models import ServicePhotos
from rest_framework import serializers

class ServicePhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServicePhotos
        fields = ['image']
        read_only_fields = ['id','service']
    