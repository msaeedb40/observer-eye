"""
Template Dashboards models for Observer-Eye Platform.
Pre-built dashboard templates.
"""
from django.db import models
from core.models import BaseModel


class DashboardTemplate(BaseModel):
    """Dashboard template definition."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('overview', 'Overview'),
            ('infrastructure', 'Infrastructure'),
            ('application', 'Application'),
            ('security', 'Security'),
            ('performance', 'Performance'),
            ('custom', 'Custom'),
        ],
        db_index=True
    )
    thumbnail = models.URLField(blank=True)
    
    # Template definition
    content = models.JSONField(default=dict, blank=True)  # Generic content field for import/export
    layout = models.JSONField(default=dict)
    widgets = models.JSONField(default=list)  # List of widget definitions
    variables = models.JSONField(default=list, blank=True)  # Template variables
    
    # Metadata
    version = models.CharField(max_length=20, default='1.0.0')
    is_official = models.BooleanField(default=False)
    downloads = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Dashboard Template'
        verbose_name_plural = 'Dashboard Templates'

    def __str__(self):
        return self.name


class TemplateInstance(BaseModel):
    """Instance of a template applied by a user."""
    template = models.ForeignKey(DashboardTemplate, on_delete=models.SET_NULL, null=True)
    user_id = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255)
    
    # Customizations
    variable_values = models.JSONField(default=dict, blank=True)
    customizations = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = 'Template Instance'
        verbose_name_plural = 'Template Instances'

    def __str__(self):
        return f"{self.name} (from {self.template.name if self.template else 'N/A'})"

class FeaturedTemplate(BaseModel):
    """Curated list of promoted templates."""
    template = models.OneToOneField(DashboardTemplate, on_delete=models.CASCADE, related_name='featured')
    order = models.IntegerField(default=0)
    promo_banner = models.URLField(blank=True)
    
    class Meta:
        verbose_name = 'Featured Template'
        verbose_name_plural = 'Featured Templates'
        ordering = ['order']

    def __str__(self):
        return f"Featured: {self.template.name}"

class VariableCatalog(BaseModel):
    """Reusable template variables."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    variable_type = models.CharField(max_length=50) # query, constant, interval
    definition = models.JSONField(default=dict)
    
    is_global = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Variable Catalog'
        verbose_name_plural = 'Variable Catalogs'

    def __str__(self):
        return self.name
