"""Settings serializers."""
from rest_framework import serializers
from .models import Setting, UserPreference, FeatureFlag, WorkspaceSettings


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_sensitive:
            data['value'] = '***HIDDEN***'
        return data


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class FeatureFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureFlag
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class WorkspaceSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceSettings
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'slug']
