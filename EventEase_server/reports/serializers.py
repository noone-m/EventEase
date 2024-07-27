from rest_framework import serializers
from .models import ReportReview, ReportService


class ReportReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReview
        fields = ['id', 'reporter', 'review', 'solved_by','is_solved', 'reason']
        read_only_fields = ['id', 'reporter', 'review', 'solved_by','is_solved']


class ReportServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportService
        fields = ['id', 'reporter', 'service', 'solved_by', 'is_solved', 'reason', 'evidence', 'resolution']
        read_only_fields = ['id', 'reporter', 'service', 'solved_by', 'is_solved']