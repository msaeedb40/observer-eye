"""Grail Observer admin."""
from django.contrib import admin
from .models import GrailEntity, GrailRelationship

@admin.register(GrailEntity)
class GrailEntityAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'entity_type', 'health_status', 'last_seen']
    list_filter = ['entity_type', 'health_status']
    search_fields = ['display_name', 'entity_id']

@admin.register(GrailRelationship)
class GrailRelationshipAdmin(admin.ModelAdmin):
    list_display = ['source', 'relationship_type', 'target']
    list_filter = ['relationship_type']
