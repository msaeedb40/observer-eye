from django.db import models
from core.models import BaseModel

class SystemResource(BaseModel):
    """System resource configuration and capacity."""
    hostname = models.CharField(max_length=255, unique=True)
    os_name = models.CharField(max_length=100)
    cpu_cores = models.IntegerField(default=1)
    memory_gb = models.FloatField(default=1.0)
    disk_gb = models.FloatField(default=10.0)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    region = models.CharField(max_length=50, default='local')
    environment = models.CharField(max_length=50, default='dev')
    
    agent_version = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, default='offline') # online, offline, degraded

    class Meta:
        verbose_name = 'System Resource'
        verbose_name_plural = 'System Resources'

    def __str__(self):
        return f"{self.hostname} ({self.ip_address})"

class KubernetesCluster(BaseModel):
    """Kubernetes Cluster configuration."""
    name = models.CharField(max_length=255, unique=True)
    api_server_url = models.URLField()
    version = models.CharField(max_length=50) # v1.28.0
    status = models.CharField(max_length=20, default='active')
    
    region = models.CharField(max_length=50, blank=True)
    provider = models.CharField(max_length=50, default='self-hosted') # aws, gcp, azure, self-hosted

    class Meta:
        verbose_name = 'Kubernetes Cluster'
        verbose_name_plural = 'Kubernetes Clusters'

    def __str__(self):
        return self.name

class KubernetesNode(BaseModel):
    """Kubernetes Node mapped to a System Resource."""
    cluster = models.ForeignKey(KubernetesCluster, on_delete=models.CASCADE, related_name='nodes')
    system_resource = models.OneToOneField(SystemResource, on_delete=models.CASCADE, related_name='k8s_node')
    
    node_role = models.CharField(max_length=50, default='worker') # control-plane, worker
    status = models.CharField(max_length=20, default='Ready')
    
    capacity_cpu = models.IntegerField(default=0) # millicores
    capacity_memory = models.BigIntegerField(default=0) # bytes

    class Meta:
        verbose_name = 'Kubernetes Node'
        verbose_name_plural = 'Kubernetes Nodes'

    def __str__(self):
        return f"{self.system_resource.hostname} ({self.node_role})"

class KubernetesPod(BaseModel):
    """Kubernetes Pod workload."""
    cluster = models.ForeignKey(KubernetesCluster, on_delete=models.CASCADE, related_name='pods')
    node = models.ForeignKey(KubernetesNode, on_delete=models.SET_NULL, null=True, related_name='pods')
    
    name = models.CharField(max_length=255)
    namespace = models.CharField(max_length=100, default='default')
    phase = models.CharField(max_length=50, default='Pending') # Pending, Running, Succeeded, Failed
    
    restart_count = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    
    labels = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'Kubernetes Pod'
        verbose_name_plural = 'Kubernetes Pods'
        unique_together = ['cluster', 'namespace', 'name']

    def __str__(self):
        return f"{self.namespace}/{self.name}"

class CloudResource(BaseModel):
    """Cloud Infrastructure Map."""
    provider = models.CharField(max_length=50) # AWS, GCP, Azure
    resource_type = models.CharField(max_length=100) # EC2, S3, Lambda
    resource_id = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    
    region = models.CharField(max_length=50)
    tags = models.JSONField(default=dict, blank=True)
    
    status = models.CharField(max_length=50, default='active')

    class Meta:
        verbose_name = 'Cloud Resource'
        verbose_name_plural = 'Cloud Resources'

    def __str__(self):
        return f"{self.provider} {self.resource_type} ({self.name})"
