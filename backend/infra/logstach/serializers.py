from rest_framework import serializers
from .models import LogPipeline, SanitizationRule

class LogPipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogPipeline
        fields = '__all__'

class SanitizationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanitizationRule
        fields = '__all__'
