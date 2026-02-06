"""
Container and Kubernetes metrics for Observer-Eye Platform.
Tracks container-level metrics: Docker, Kubernetes pods, and GPU workloads.
"""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class ContainerMetric(BaseModel, ObservabilityMixin):
    """Docker/K8s container metrics."""
    host = models.CharField(max_length=255, db_index=True)
    container_id = models.CharField(max_length=64, db_index=True)
    container_name = models.CharField(max_length=255)
    image = models.CharField(max_length=500)
    namespace = models.CharField(max_length=255, blank=True)  # K8s namespace
    pod_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('running', 'Running'),
            ('stopped', 'Stopped'),
            ('paused', 'Paused'),
            ('restarting', 'Restarting'),
            ('created', 'Created'),
            ('exited', 'Exited'),
        ],
        default='running'
    )
    
    # CPU
    cpu_percent = models.FloatField(default=0.0)
    cpu_limit_cores = models.FloatField(null=True, blank=True)
    cpu_request_cores = models.FloatField(null=True, blank=True)
    
    # Memory
    memory_usage_bytes = models.BigIntegerField(default=0)
    memory_limit_bytes = models.BigIntegerField(default=0)
    memory_request_bytes = models.BigIntegerField(null=True, blank=True)
    memory_percent = models.FloatField(default=0.0)
    
    # Network
    network_rx_bytes = models.BigIntegerField(default=0)
    network_tx_bytes = models.BigIntegerField(default=0)
    
    # Container lifecycle
    restart_count = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Container Metric'
        verbose_name_plural = 'Container Metrics'
        indexes = [
            models.Index(fields=['host', 'container_id', 'timestamp']),
            models.Index(fields=['namespace', 'pod_name', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.container_name} ({self.status})"


class KubernetesEvent(BaseModel):
    """Kubernetes cluster events."""
    cluster = models.CharField(max_length=255, db_index=True)
    namespace = models.CharField(max_length=255, db_index=True)
    kind = models.CharField(max_length=50, db_index=True)  # Pod, Deployment, Node, Service
    name = models.CharField(max_length=255)
    uid = models.CharField(max_length=64, blank=True)
    
    event_type = models.CharField(
        max_length=50,
        choices=[
            ('Normal', 'Normal'),
            ('Warning', 'Warning'),
        ],
        default='Normal'
    )
    reason = models.CharField(max_length=100)
    message = models.TextField()
    
    # Event timing
    first_timestamp = models.DateTimeField(null=True, blank=True)
    last_timestamp = models.DateTimeField(null=True, blank=True)
    count = models.IntegerField(default=1)
    
    # Source
    source_component = models.CharField(max_length=100, blank=True)
    source_host = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name = 'Kubernetes Event'
        verbose_name_plural = 'Kubernetes Events'
        indexes = [
            models.Index(fields=['cluster', 'namespace', 'kind']),
        ]

    def __str__(self):
        return f"{self.kind}/{self.name}: {self.reason}"


class KubernetesPod(BaseModel):
    """Kubernetes pod status and metadata."""
    cluster = models.CharField(max_length=255, db_index=True)
    namespace = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    uid = models.CharField(max_length=64, unique=True)
    
    phase = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Running', 'Running'),
            ('Succeeded', 'Succeeded'),
            ('Failed', 'Failed'),
            ('Unknown', 'Unknown'),
        ],
        default='Unknown'
    )
    
    # Node assignment
    node_name = models.CharField(max_length=255, blank=True)
    host_ip = models.GenericIPAddressField(null=True, blank=True)
    pod_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Labels and annotations
    labels = models.JSONField(default=dict, blank=True)
    annotations = models.JSONField(default=dict, blank=True)
    
    # Container counts
    container_count = models.IntegerField(default=0)
    ready_containers = models.IntegerField(default=0)
    
    # Timestamps
    start_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Kubernetes Pod'
        verbose_name_plural = 'Kubernetes Pods'
        unique_together = ['cluster', 'namespace', 'name']

    def __str__(self):
        return f"{self.namespace}/{self.name} ({self.phase})"


class GPUMetric(BaseModel, ObservabilityMixin):
    """GPU metrics for ML/AI workloads."""
    host = models.CharField(max_length=255, db_index=True)
    gpu_index = models.IntegerField()
    gpu_uuid = models.CharField(max_length=64, blank=True)
    gpu_name = models.CharField(max_length=255)
    
    # Utilization
    utilization_percent = models.FloatField(default=0.0)
    memory_utilization_percent = models.FloatField(default=0.0)
    
    # Memory
    memory_used_mb = models.IntegerField(default=0)
    memory_total_mb = models.IntegerField(default=0)
    memory_free_mb = models.IntegerField(default=0)
    
    # Power and temperature
    temperature_celsius = models.FloatField(default=0.0)
    power_watts = models.FloatField(default=0.0)
    power_limit_watts = models.FloatField(null=True, blank=True)
    
    # Processes
    running_processes = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'GPU Metric'
        verbose_name_plural = 'GPU Metrics'
        indexes = [
            models.Index(fields=['host', 'gpu_index', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.gpu_name} (GPU {self.gpu_index}) - {self.utilization_percent}%"
