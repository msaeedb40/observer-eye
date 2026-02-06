from rest_framework import serializers
from .models import TrafficStats, RouteAnalytics, LoadBalancerStats
from .rum import CoreWebVitals, UserSession, PageView, FrontendError, ResourceTiming
from .synthetic import SyntheticMonitor, SyntheticResult


class TrafficStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficStats
        fields = '__all__'


class RouteAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteAnalytics
        fields = '__all__'


class LoadBalancerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadBalancerStats
        fields = '__all__'


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'started_at']


class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class CoreWebVitalsSerializer(serializers.ModelSerializer):
    vitals_status = serializers.ReadOnlyField()

    class Meta:
        model = CoreWebVitals
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class FrontendErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontendError
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'first_seen', 'last_seen']


class ResourceTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceTiming
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SyntheticMonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyntheticMonitor
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SyntheticResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyntheticResult
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
