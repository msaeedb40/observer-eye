from rest_framework import serializers
from .models import CloudProvider, CloudRegion

class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = '__all__'

class CloudRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudRegion
        fields = '__all__'
