"""Reliability metrics for Observer-Eye Platform."""
from django.db.models import Avg, F, ExpressionWrapper, fields
from django.utils import timezone
from .models import Alert

def calculate_reliability_metrics():
    """
    Calculate Mean Time to Detect (MTTD), Mean Time to Resolve (MTTR), 
    and Mean Time to Silence/Acknowledge (MTTS).
    """
    resolved_alerts = Alert.objects.filter(state='resolved', resolved_at__isnull=False, event_start_at__isnull=False)
    acknowledged_alerts = Alert.objects.filter(acknowledged_at__isnull=False, event_start_at__isnull=False)

    # MTTD: Average of (Alert.started_at - Alert.event_start_at)
    mttd = Alert.objects.filter(event_start_at__isnull=False).annotate(
        detection_time=ExpressionWrapper(F('started_at') - F('event_start_at'), output_field=fields.DurationField())
    ).aggregate(Avg('detection_time'))['detection_time__avg']

    # MTTR: Average of (Alert.resolved_at - Alert.started_at)
    mttr = resolved_alerts.annotate(
        resolution_time=ExpressionWrapper(F('resolved_at') - F('started_at'), output_field=fields.DurationField())
    ).aggregate(Avg('resolution_time'))['resolution_time__avg']

    # MTTS (Mean Time to Acknowledge): Average of (Alert.acknowledged_at - Alert.started_at)
    mtts = acknowledged_alerts.annotate(
        acknowledgment_time=ExpressionWrapper(F('acknowledged_at') - F('started_at'), output_field=fields.DurationField())
    ).aggregate(Avg('acknowledgment_time'))['acknowledgment_time__avg']

    return {
        'mttd_seconds': mttd.total_seconds() if mttd else 0,
        'mttr_seconds': mttr.total_seconds() if mttr else 0,
        'mtts_seconds': mtts.total_seconds() if mtts else 0,
        'timestamp': timezone.now().isoformat()
    }
