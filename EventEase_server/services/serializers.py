from .models import FoodService
from rest_framework import serializers

class FoodServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodService
        fields = '__all__'
    