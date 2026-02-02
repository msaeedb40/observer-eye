"""Grail Observer serializers."""
from rest_framework import serializers
from .models import GrailEntity, GrailRelationship


class GrailRelationshipSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.display_name', read_only=True)
    target_name = serializers.CharField(source='target.display_name', read_only=True)
    
    class Meta:
        model = GrailRelationship
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class GrailEntitySerializer(serializers.ModelSerializer):
    outgoing_relationships = GrailRelationshipSerializer(many=True, read_only=True)
    incoming_relationships = GrailRelationshipSerializer(many=True, read_only=True)
    
    class Meta:
        model = GrailEntity
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class GrailEntityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrailEntity
        fields = ['id', 'entity_id', 'entity_type', 'display_name', 'health_status', 'last_seen']
