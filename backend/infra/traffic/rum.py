"""
Real User Monitoring (RUM) and Core Web Vitals models for Observer-Eye Platform.
Tracks frontend performance, user sessions, and Core Web Vitals metrics.
"""
from django.db import models
from core.models import BaseModel


class CoreWebVitals(BaseModel):
    """Core Web Vitals metrics (LCP, FID, CLS, INP, TTFB)."""
    session_id = models.CharField(max_length=64, db_index=True)
    page_url = models.URLField(max_length=2048, db_index=True)
    page_path = models.CharField(max_length=512, db_index=True)
    
    # Core Web Vitals
    lcp_ms = models.FloatField(null=True, blank=True, help_text="Largest Contentful Paint (ms)")
    fid_ms = models.FloatField(null=True, blank=True, help_text="First Input Delay (ms)")
    cls = models.FloatField(null=True, blank=True, help_text="Cumulative Layout Shift")
    inp_ms = models.FloatField(null=True, blank=True, help_text="Interaction to Next Paint (ms)")
    ttfb_ms = models.FloatField(null=True, blank=True, help_text="Time to First Byte (ms)")
    
    # Additional timing
    fcp_ms = models.FloatField(null=True, blank=True, help_text="First Contentful Paint (ms)")
    dom_interactive_ms = models.FloatField(null=True, blank=True)
    dom_complete_ms = models.FloatField(null=True, blank=True)
    load_event_ms = models.FloatField(null=True, blank=True)
    
    # Context
    user_agent = models.TextField(blank=True)
    browser = models.CharField(max_length=100, blank=True)
    browser_version = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(
        max_length=20,
        choices=[
            ('desktop', 'Desktop'),
            ('mobile', 'Mobile'),
            ('tablet', 'Tablet'),
        ],
        default='desktop'
    )
    
    connection_type = models.CharField(max_length=20, blank=True)  # 4g, wifi, etc
    effective_bandwidth_mbps = models.FloatField(null=True, blank=True)
    
    # Geo
    country_code = models.CharField(max_length=2, blank=True)
    region = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Core Web Vitals'
        verbose_name_plural = 'Core Web Vitals'
        indexes = [
            models.Index(fields=['page_path', 'created_at']),
            models.Index(fields=['device_type', 'created_at']),
        ]

    def __str__(self):
        return f"{self.page_path} - LCP: {self.lcp_ms}ms"

    @property
    def vitals_status(self):
        """Return pass/fail status based on Google thresholds."""
        status = {'lcp': 'good', 'fid': 'good', 'cls': 'good', 'inp': 'good'}
        if self.lcp_ms:
            if self.lcp_ms > 4000:
                status['lcp'] = 'poor'
            elif self.lcp_ms > 2500:
                status['lcp'] = 'needs_improvement'
        if self.fid_ms:
            if self.fid_ms > 300:
                status['fid'] = 'poor'
            elif self.fid_ms > 100:
                status['fid'] = 'needs_improvement'
        if self.cls is not None:
            if self.cls > 0.25:
                status['cls'] = 'poor'
            elif self.cls > 0.1:
                status['cls'] = 'needs_improvement'
        if self.inp_ms:
            if self.inp_ms > 500:
                status['inp'] = 'poor'
            elif self.inp_ms > 200:
                status['inp'] = 'needs_improvement'
        return status


class UserSession(BaseModel):
    """User session tracking."""
    session_id = models.CharField(max_length=64, unique=True, db_index=True)
    user_id = models.CharField(max_length=255, blank=True, db_index=True)
    
    # Session timing
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)
    
    # Activity
    page_views = models.IntegerField(default=0)
    interactions = models.IntegerField(default=0)
    errors_count = models.IntegerField(default=0)
    
    # Funnel
    entry_page = models.CharField(max_length=512, blank=True)
    exit_page = models.CharField(max_length=512, blank=True)
    referrer = models.URLField(max_length=2048, blank=True)
    
    # Context
    device_type = models.CharField(max_length=20, default='desktop')
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    country_code = models.CharField(max_length=2, blank=True)
    
    # Session quality
    is_bounce = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        ordering = ['-started_at']

    def __str__(self):
        return f"Session {self.session_id[:8]}... ({self.page_views} pages)"


class PageView(BaseModel):
    """Individual page view events."""
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='page_view_set')
    page_url = models.URLField(max_length=2048)
    page_path = models.CharField(max_length=512, db_index=True)
    page_title = models.CharField(max_length=512, blank=True)
    
    # Timing
    load_time_ms = models.IntegerField(default=0)
    time_on_page_seconds = models.IntegerField(default=0)
    
    # Interaction
    scroll_depth_percent = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    
    # Navigation
    previous_page = models.CharField(max_length=512, blank=True)
    
    class Meta:
        verbose_name = 'Page View'
        verbose_name_plural = 'Page Views'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.page_path}"


class FrontendError(BaseModel):
    """JavaScript and frontend errors."""
    session_id = models.CharField(max_length=64, db_index=True)
    page_url = models.URLField(max_length=2048)
    
    error_type = models.CharField(max_length=100, db_index=True)  # TypeError, SyntaxError, etc
    error_message = models.TextField()
    stack_trace = models.TextField(blank=True)
    
    # Source info
    filename = models.CharField(max_length=512, blank=True)
    line_number = models.IntegerField(null=True, blank=True)
    column_number = models.IntegerField(null=True, blank=True)
    
    # Context
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    
    # Grouping
    error_hash = models.CharField(max_length=64, db_index=True)  # For deduplication
    occurrences = models.IntegerField(default=1)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Frontend Error'
        verbose_name_plural = 'Frontend Errors'
        ordering = ['-last_seen']

    def __str__(self):
        return f"{self.error_type}: {self.error_message[:50]}"


class ResourceTiming(BaseModel):
    """Resource loading performance."""
    session_id = models.CharField(max_length=64, db_index=True)
    page_url = models.URLField(max_length=2048)
    
    resource_url = models.URLField(max_length=2048)
    resource_type = models.CharField(
        max_length=20,
        choices=[
            ('script', 'Script'),
            ('stylesheet', 'Stylesheet'),
            ('image', 'Image'),
            ('font', 'Font'),
            ('xhr', 'XHR'),
            ('fetch', 'Fetch'),
            ('other', 'Other'),
        ],
        db_index=True
    )
    
    # Timing
    start_time_ms = models.FloatField()
    duration_ms = models.FloatField()
    dns_time_ms = models.FloatField(default=0)
    connect_time_ms = models.FloatField(default=0)
    ssl_time_ms = models.FloatField(default=0)
    ttfb_ms = models.FloatField(default=0)
    download_time_ms = models.FloatField(default=0)
    
    # Size
    transfer_size_bytes = models.IntegerField(default=0)
    encoded_body_size = models.IntegerField(default=0)
    decoded_body_size = models.IntegerField(default=0)
    
    # Status
    response_status = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Resource Timing'
        verbose_name_plural = 'Resource Timings'

    def __str__(self):
        return f"{self.resource_type}: {self.duration_ms}ms"
