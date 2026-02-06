from django.db import models
from core.models import BaseModel

class ServiceRegistry(BaseModel):
    """Catalog of microservices."""
    name = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=50)
    language = models.CharField(max_length=50) # python, go, java
    framework = models.CharField(max_length=100) # django, spring
    
    owner_team = models.CharField(max_length=100, blank=True)
    repo_url = models.URLField(blank=True)
    
    status = models.CharField(max_length=20, default='active')

    class Meta:
        verbose_name = 'Service Registry'
        verbose_name_plural = 'Service Registries'

    def __str__(self):
        return self.name

class DependencyMap(BaseModel):
    """Service-to-service dependency."""
    consumer = models.ForeignKey(ServiceRegistry, on_delete=models.CASCADE, related_name='consumes')
    provider = models.ForeignKey(ServiceRegistry, on_delete=models.CASCADE, related_name='provided_to')
    
    dependency_type = models.CharField(max_length=50, default='http') # http, grpc, db, queue
    is_critical = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Dependency Map'
        verbose_name_plural = 'Dependency Maps'
        unique_together = ['consumer', 'provider']

    def __str__(self):
        return f"{self.consumer.name} -> {self.provider.name}"

class DeploymentEvent(BaseModel):
    """CD Pipeline deployment event."""
    service = models.ForeignKey(ServiceRegistry, on_delete=models.CASCADE, related_name='deployments')
    version = models.CharField(max_length=50)
    environment = models.CharField(max_length=50)
    
    status = models.CharField(max_length=20, default='in_progress')
    triggered_by = models.CharField(max_length=100) # User or Git Commit
    
    commit_hash = models.CharField(max_length=100, blank=True)
    pipeline_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Deployment Event'
        verbose_name_plural = 'Deployment Events'

    def __str__(self):
        return f"{self.service.name} {self.version} ({self.status})"

class ConfigWatcher(BaseModel):
    """Configuration or Secret change detection."""
    source_type = models.CharField(max_length=50) # env_var, file, secret_manager
    source_name = models.CharField(max_length=255)
    
    key = models.CharField(max_length=255)
    change_type = models.CharField(max_length=20) # added, modified, deleted
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Config Watcher'
        verbose_name_plural = 'Config Watchers'

    def __str__(self):
        return f"{self.key} ({self.change_type})"

class KubernetesPod(BaseModel):
    """K8s Pod mapping for services."""
    pod_name = models.CharField(max_length=255)
    namespace = models.CharField(max_length=255)
    node_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    service = models.ForeignKey(ServiceRegistry, on_delete=models.SET_NULL, null=True, blank=True, related_name='pods')

    class Meta:
        verbose_name = 'Kubernetes Pod'
        verbose_name_plural = 'Kubernetes Pods'

    def __str__(self):
        return f"{self.namespace}/{self.pod_name}"

class KubernetesDeployment(BaseModel):
    """K8s Deployment tracking."""
    name = models.CharField(max_length=255)
    namespace = models.CharField(max_length=255)
    replicas = models.IntegerField(default=1)
    available_replicas = models.IntegerField(default=0)
    
    service = models.ForeignKey(ServiceRegistry, on_delete=models.SET_NULL, null=True, blank=True, related_name='k8s_deployments')

    class Meta:
        verbose_name = 'Kubernetes Deployment'
        verbose_name_plural = 'Kubernetes Deployments'

    def __str__(self):
        return f"{self.namespace}/{self.name}"
