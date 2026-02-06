"""Notification serializers."""
from rest_framework import serializers
from .models import NotificationChannel, AlertRule, Alert, NotificationHistory


class NotificationChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationChannel
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AlertRuleSerializer(serializers.ModelSerializer):
    channels = NotificationChannelSerializer(many=True, read_only=True)
    channel_ids = serializers.PrimaryKeyRelatedField(
        queryset=NotificationChannel.objects.all(),
        many=True,
        write_only=True,
        source='channels',
        required=False
    )
    
    def create(self, validated_data):
        # Handle cases where 'channels' might be passed instead of channel_ids (compat)
        channels_data = self.initial_data.get('channels', [])
        if channels_data and not validated_data.get('channels'):
             # If exact IDs passed in channels field, use them
             if isinstance(channels_data, list) and all(isinstance(x, int) for x in channels_data):
                 validated_data['channels'] = NotificationChannel.objects.filter(id__in=channels_data)
        
        return super().create(validated_data)
    
    class Meta:
        model = AlertRule
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AlertSerializer(serializers.ModelSerializer):
    rule_name = serializers.CharField(source='rule.name', read_only=True, required=False)
    # Computed fields to match API contract
    channels = serializers.SerializerMethodField(read_only=True)
    active = serializers.BooleanField(source='enabled', required=False)
    
    def get_channels(self, obj):
        """Convert dispatch_channels list to channel dictionary."""
        channels = {}
        for channel_type in (obj.dispatch_channels or []):
            config = {}
            if channel_type == "email" and obj.email_config:
                config = obj.email_config
            elif channel_type == "slack" and obj.slack_config:
                config = obj.slack_config
            channels[channel_type] = [config] if config else []
        return channels
    
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'started_at']
        extra_kwargs = {
            'rule': {'required': False, 'allow_null': True},
            'message': {'required': False},
            'severity': {'required': False},
        }


class NotificationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationHistory
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
