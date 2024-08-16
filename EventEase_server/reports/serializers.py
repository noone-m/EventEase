from rest_framework import serializers
from .models import ReportReview, ReportService
from accounts.serializers import AdminUserSerializer
from services.serializers import ServiceSerializer
from reviews.serializers import ReviewSerializer

class ReportReviewSerializer(serializers.ModelSerializer):
    reporter = AdminUserSerializer(read_only=True)
    review = ReviewSerializer(read_only=True)
    class Meta:
        model = ReportReview
        fields = ['id', 'reporter', 'review', 'solved_by','is_solved', 'reason']
        read_only_fields = ['id', 'reporter', 'review', 'solved_by','is_solved']


class ReportServiceSerializer(serializers.ModelSerializer):
    reporter = AdminUserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    class Meta:
        model = ReportService
        fields = ['id', 'reporter', 'service', 'solved_by', 'is_solved', 'reason', 'evidence', 'resolution']
        read_only_fields = ['id', 'reporter', 'service', 'solved_by', 'is_solved']