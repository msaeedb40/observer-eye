"""Insights Observer serializers."""
from rest_framework import serializers
from .models import Insight, AnomalyDetection


class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AnomalyDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnomalyDetection
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'detected_at']
