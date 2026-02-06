from django.db import models
from core.models import BaseModel

class UserIdentity(BaseModel):
    """Extended user identity metadata."""
    user_id = models.CharField(max_length=255, unique=True, db_index=True) # ID from external auth provider
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default='viewer')
    department = models.CharField(max_length=100, blank=True)
    
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User Identity'
        verbose_name_plural = 'User Identities'

    def __str__(self):
        return f"{self.email} ({self.role})"

class AccessLog(BaseModel):
    """Log of user authentication and access events."""
    user = models.ForeignKey(UserIdentity, on_delete=models.CASCADE, related_name='access_logs')
    ip_address = models.GenericIPAddressField()
    action = models.CharField(max_length=50) # login, logout, failed_login
    resource = models.CharField(max_length=255, blank=True)
    user_agent = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='success')
    
    class Meta:
        verbose_name = 'Access Log'
        verbose_name_plural = 'Access Logs'

    def __str__(self):
        return f"{self.user.email} - {self.action}"

class UserGroup(BaseModel):
    """RBAC User Group."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=list)
    
    users = models.ManyToManyField(UserIdentity, related_name='groups')

    class Meta:
        verbose_name = 'User Group'
        verbose_name_plural = 'User Groups'

    def __str__(self):
        return self.name

class MFAStatus(BaseModel):
    """Multi-Factor Authentication status."""
    user = models.OneToOneField(UserIdentity, on_delete=models.CASCADE, related_name='mfa_status')
    is_enabled = models.BooleanField(default=False)
    method = models.CharField(max_length=50, default='none') # app, sms, hardware
    
    last_verified = models.DateTimeField(null=True, blank=True)
    backup_codes_remaining = models.IntegerField(default=10)

    class Meta:
        verbose_name = 'MFA Status'
        verbose_name_plural = 'MFA Statuses'

    def __str__(self):
        return f"{self.user.email} (MFA: {self.is_enabled})"
