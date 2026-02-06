from django.db import models
from core.models import BaseModel

class ThreatEvent(BaseModel):
    """Security threat detected by IDS/IPS or analysis."""
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='security_threatevent_created'
    )
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    severity = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')],
        default='low'
    )
    threat_type = models.CharField(max_length=100) # DDoS, SQL Injection, Brute Force
    description = models.TextField()
    
    status = models.CharField(
        max_length=20,
        choices=[('detected', 'Detected'), ('blocked', 'Blocked'), ('mitigated', 'Mitigated')],
        default='detected'
    )
    
    class Meta:
        verbose_name = 'Threat Event'
        verbose_name_plural = 'Threat Events'

    def __str__(self):
        return f"{self.threat_type} ({self.source_ip})"

class AuditTrail(BaseModel):
    """Immutable record of system changes."""
    actor = models.CharField(max_length=255) # user or service
    action = models.CharField(max_length=100)
    target = models.CharField(max_length=255)
    changes = models.JSONField(default=dict) # before/after
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Audit Trail'
        verbose_name_plural = 'Audit Trails'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor} -> {self.action}"

class VulnerabilityScan(BaseModel):
    """Security vulnerability scan result."""
    target = models.CharField(max_length=255) # Host or Image
    scan_tpe = models.CharField(max_length=50, default='static') # static, dynamic
    scanner_name = models.CharField(max_length=100) # Trivy, Clair
    
    cve_id = models.CharField(max_length=50, db_index=True)
    severity = models.CharField(max_length=20)
    description = models.TextField()
    
    status = models.CharField(max_length=20, default='open') # open, fixed, ignored

    class Meta:
        verbose_name = 'Vulnerability Scan'
        verbose_name_plural = 'Vulnerability Scans'

    def __str__(self):
        return f"{self.cve_id} on {self.target}"

class CompliancePolicy(BaseModel):
    """Compliance benchmark check."""
    name = models.CharField(max_length=255)
    framework = models.CharField(max_length=100) # CIS, GDPR, PCI-DSS
    description = models.TextField()
    
    status = models.CharField(max_length=20, default='active')
    last_check_status = models.CharField(max_length=20, default='unknown') # pass, fail
    last_check_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Compliance Policy'
        verbose_name_plural = 'Compliance Policies'

    def __str__(self):
        return f"{self.framework} - {self.name}"
