from rest_framework import serializers
from .models import UserIdentity, AccessLog, UserGroup, MFAStatus

class UserIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIdentity
        fields = '__all__'

class AccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLog
        fields = '__all__'

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'

class MFAStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MFAStatus
        fields = '__all__'
