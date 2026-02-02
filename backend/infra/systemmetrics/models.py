"""
System Metrics models for Observer-Eye Platform.
Tracks system-level metrics: CPU, memory, disk, processes.
"""
from django.db import models
from core.models import BaseModel, ObservabilityMixin


class SystemMetric(BaseModel, ObservabilityMixin):
    """System-level metrics."""
    host = models.CharField(max_length=255, db_index=True)
    hostname = models.CharField(max_length=255, blank=True)
    
    # CPU
    cpu_percent = models.FloatField(default=0.0)
    cpu_count = models.IntegerField(default=0)
    load_avg_1min = models.FloatField(default=0.0)
    load_avg_5min = models.FloatField(default=0.0)
    load_avg_15min = models.FloatField(default=0.0)
    
    # Memory
    memory_total_bytes = models.BigIntegerField(default=0)
    memory_available_bytes = models.BigIntegerField(default=0)
    memory_used_bytes = models.BigIntegerField(default=0)
    memory_percent = models.FloatField(default=0.0)
    
    # Swap
    swap_total_bytes = models.BigIntegerField(default=0)
    swap_used_bytes = models.BigIntegerField(default=0)
    swap_percent = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = 'System Metric'
        verbose_name_plural = 'System Metrics'
        indexes = [
            models.Index(fields=['host', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.host} - CPU: {self.cpu_percent}%, Mem: {self.memory_percent}%"


class DiskMetric(BaseModel, ObservabilityMixin):
    """Disk metrics per mount point."""
    host = models.CharField(max_length=255, db_index=True)
    mount_point = models.CharField(max_length=255, db_index=True)
    device = models.CharField(max_length=255)
    
    total_bytes = models.BigIntegerField(default=0)
    used_bytes = models.BigIntegerField(default=0)
    free_bytes = models.BigIntegerField(default=0)
    usage_percent = models.FloatField(default=0.0)
    
    # I/O
    read_bytes = models.BigIntegerField(default=0)
    write_bytes = models.BigIntegerField(default=0)
    read_count = models.BigIntegerField(default=0)
    write_count = models.BigIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Disk Metric'
        verbose_name_plural = 'Disk Metrics'

    def __str__(self):
        return f"{self.host}:{self.mount_point} - {self.usage_percent}%"


class ProcessMetric(BaseModel, ObservabilityMixin):
    """Process-level metrics."""
    host = models.CharField(max_length=255, db_index=True)
    pid = models.IntegerField()
    name = models.CharField(max_length=255, db_index=True)
    status = models.CharField(max_length=50)
    
    cpu_percent = models.FloatField(default=0.0)
    memory_percent = models.FloatField(default=0.0)
    memory_rss_bytes = models.BigIntegerField(default=0)
    threads = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Process Metric'
        verbose_name_plural = 'Process Metrics'

    def __str__(self):
        return f"{self.name} (PID: {self.pid})"
