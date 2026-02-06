from rest_framework import serializers
from .models import CloudMetric, CloudCost

class CloudMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudMetric
        fields = '__all__'

class CloudCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudCost
        fields = '__all__'
