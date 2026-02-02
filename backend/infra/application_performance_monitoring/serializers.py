"""APM serializers."""
from rest_framework import serializers
from .models import APMTransaction, APMSpan, APMError


class APMSpanSerializer(serializers.ModelSerializer):
    class Meta:
        model = APMSpan
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class APMTransactionSerializer(serializers.ModelSerializer):
    spans = APMSpanSerializer(many=True, read_only=True)
    
    class Meta:
        model = APMTransaction
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class APMTransactionListSerializer(serializers.ModelSerializer):
    span_count = serializers.SerializerMethodField()
    
    class Meta:
        model = APMTransaction
        fields = ['id', 'app_name', 'transaction_name', 'duration_ms', 'result', 'http_status_code', 'timestamp', 'span_count']
    
    def get_span_count(self, obj):
        return obj.spans.count()


class APMErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = APMError
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
