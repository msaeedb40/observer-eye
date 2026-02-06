from django.db import models
from core.models import BaseModel

class CloudProvider(BaseModel):
    """AWS, Azure, GCP provider metadata."""
    name = models.CharField(max_length=100)
    provider_type = models.CharField(max_length=50) # aws, azure, gcp, digitalocean
    account_id = models.CharField(max_length=100)
    secret_name = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Cloud Provider'
        verbose_name_plural = 'Cloud Providers'

    def __str__(self):
        return f"{self.name} ({self.provider_type})"

class CloudRegion(BaseModel):
    """Cloud regions and availability zones."""
    provider = models.ForeignKey(CloudProvider, on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(max_length=100) # us-east-1, eu-central-1
    status = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Cloud Region'
        verbose_name_plural = 'Cloud Regions'

    def __str__(self):
        return f"{self.provider.name} - {self.name}"
