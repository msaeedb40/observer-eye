"""
Grail Observer models for Observer-Eye Platform.
Grail observer integration.
"""
from django.db import models
from core.models import BaseModel


class GrailEntity(BaseModel):
    """Grail entity for topology mapping."""
    entity_id = models.CharField(max_length=255, unique=True, db_index=True)
    entity_type = models.CharField(max_length=100, db_index=True)  # host, service, process, etc.
    display_name = models.CharField(max_length=255)
    
    # Relationships
    parent_id = models.CharField(max_length=255, blank=True, db_index=True)
    
    # Properties
    properties = models.JSONField(default=dict, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Health
    health_status = models.CharField(
        max_length=20,
        choices=[
            ('healthy', 'Healthy'),
            ('degraded', 'Degraded'),
            ('unhealthy', 'Unhealthy'),
            ('unknown', 'Unknown'),
        ],
        default='unknown',
        db_index=True
    )
    last_seen = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Grail Entity'
        verbose_name_plural = 'Grail Entities'

    def __str__(self):
        return f"{self.display_name} ({self.entity_type})"


class GrailRelationship(BaseModel):
    """Relationship between Grail entities."""
    source = models.ForeignKey(GrailEntity, on_delete=models.CASCADE, related_name='outgoing_relationships')
    target = models.ForeignKey(GrailEntity, on_delete=models.CASCADE, related_name='incoming_relationships')
    relationship_type = models.CharField(max_length=100)  # runs_on, depends_on, calls, etc.
    
    class Meta:
        verbose_name = 'Grail Relationship'
        verbose_name_plural = 'Grail Relationships'
        unique_together = ['source', 'target', 'relationship_type']

    def __str__(self):
        return f"{self.source.display_name} -> {self.target.display_name}"
