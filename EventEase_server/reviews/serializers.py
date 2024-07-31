from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.models import User
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField() # to get the name of the user and not the id

    # using the above line of code generated a conflict between the user variable here and the user field in the model
    class Meta:
        model = Review
        fields = ['id', 'user', 'service', 'rating', 'comment', 'created_at', 'updated_at', 'user_name', 'avg_rating']
        read_only_fields = ['id', 'user', 'service', 'created_at', 'updated_at', 'user_name', 'avg_rating']

    def validate_rating(self, value):
        if value<0 or value>5:
            raise serializers.ValidationError("Rating should be from 0 to 5")
        return value
    
    def get_user_name(self,review):
        user = review.user
        return user.first_name + ' ' + user.last_name
