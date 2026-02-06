from django.db import models
from core.models import BaseModel, ObservabilityMixin
from cloud.models import CloudProvider

class CloudMetric(BaseModel, ObservabilityMixin):
    """Cloud-level metrics (RDS, S3, ELB)."""
    provider = models.ForeignKey(CloudProvider, on_delete=models.CASCADE, related_name='metrics')
    resource_id = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=100)
    metric_name = models.CharField(max_length=255)
    value = models.FloatField()
    unit = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Cloud Metric'
        verbose_name_plural = 'Cloud Metrics'

    def __str__(self):
        return f"{self.resource_id} : {self.metric_name}"

class CloudCost(BaseModel):
    """Cloud cost allocation and forecasting."""
    provider = models.ForeignKey(CloudProvider, on_delete=models.CASCADE, related_name='costs')
    resource_id = models.CharField(max_length=255, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=4)
    currency = models.CharField(max_length=10, default='USD')
    usage_type = models.CharField(max_length=100)
    
    billing_period_start = models.DateTimeField(null=True, blank=True)
    billing_period_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Cloud Cost'
        verbose_name_plural = 'Cloud Costs'

    def __str__(self):
        return f"{self.provider.name} Cost: {self.cost} {self.currency}"
