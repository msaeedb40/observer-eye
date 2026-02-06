"""
Celery Tasks for Observer-Eye Telemetry Processing.
Async task processing for telemetry data.
"""
import os
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Try to import Celery
try:
    from celery import Celery
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    logger.warning("Celery not installed. Task processing will be disabled.")

# Initialize Celery app
if CELERY_AVAILABLE:
    app = Celery(
        'observer_eye',
        broker=os.getenv('CELERY_BROKER', 'redis://redis:6379/1'),
        backend=os.getenv('CELERY_BACKEND', 'redis://redis:6379/2')
    )
    
    # Celery configuration
    app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_routes={
            'telemetry.celery_tasks.process_metrics_batch': {'queue': 'metrics'},
            'telemetry.celery_tasks.process_logs_batch': {'queue': 'logs'},
            'telemetry.celery_tasks.process_traces_batch': {'queue': 'traces'},
            'telemetry.celery_tasks.evaluate_alert_rules': {'queue': 'alerts'},
            'telemetry.celery_tasks.run_anomaly_detection': {'queue': 'ml'},
        }
    )


def celery_task(func):
    """Decorator that only applies @app.task if Celery is available."""
    if CELERY_AVAILABLE:
        return app.task(func)
    return func


@celery_task
def process_metrics_batch(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process a batch of metrics asynchronously.
    
    Steps:
    1. Validate and normalize metrics
    2. Enrich with context (service, namespace)
    3. Forward to backend via HTTP
    4. Trigger alert evaluation if thresholds exceeded
    """
    import httpx
    
    backend_url = os.getenv('BACKEND_URL', 'http://backend:8000')
    processed = 0
    errors = 0
    
    for metric in batch:
        try:
            # Normalize metric
            normalized = {
                'name': metric.get('name', 'unknown'),
                'value': float(metric.get('value', 0)),
                'unit': metric.get('unit', ''),
                'source': metric.get('source', 'unknown'),
                'labels': metric.get('labels', {}),
                'timestamp': metric.get('timestamp') or datetime.now(timezone.utc).isoformat(),
            }
            
            # POST to backend
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"{backend_url}/api/core/metrics/",
                    json=normalized
                )
                if response.status_code in (200, 201):
                    processed += 1
                else:
                    errors += 1
                    logger.error(f"Failed to post metric: {response.status_code}")
        except Exception as e:
            errors += 1
            logger.error(f"Error processing metric: {e}")
    
    return {'processed': processed, 'errors': errors}


@celery_task
def process_logs_batch(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process a batch of log entries asynchronously."""
    import httpx
    
    backend_url = os.getenv('BACKEND_URL', 'http://backend:8000')
    processed = 0
    errors = 0
    
    for log in batch:
        try:
            normalized = {
                'level': log.get('level', 'info'),
                'message': log.get('message', ''),
                'source': log.get('source', 'unknown'),
                'logger_name': log.get('logger_name', ''),
                'trace_id': log.get('trace_id', ''),
                'span_id': log.get('span_id', ''),
                'labels': log.get('labels', {}),
                'timestamp': log.get('timestamp') or datetime.now(timezone.utc).isoformat(),
            }
            
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"{backend_url}/api/core/logs/",
                    json=normalized
                )
                if response.status_code in (200, 201):
                    processed += 1
                else:
                    errors += 1
        except Exception as e:
            errors += 1
            logger.error(f"Error processing log: {e}")
    
    return {'processed': processed, 'errors': errors}


@celery_task
def process_traces_batch(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process a batch of traces with span correlation."""
    import httpx
    
    backend_url = os.getenv('BACKEND_URL', 'http://backend:8000')
    processed = 0
    errors = 0
    
    for trace in traces:
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"{backend_url}/api/core/traces/",
                    json=trace
                )
                if response.status_code in (200, 201):
                    processed += 1
                else:
                    errors += 1
        except Exception as e:
            errors += 1
            logger.error(f"Error processing trace: {e}")
    
    return {'processed': processed, 'errors': errors}


@celery_task
def correlate_traces(trace_id: str) -> Dict[str, Any]:
    """
    Correlate spans within a trace and update trace duration.
    """
    import httpx
    
    backend_url = os.getenv('BACKEND_URL', 'http://backend:8000')
    
    try:
        with httpx.Client(timeout=30.0) as client:
            # Get trace
            response = client.get(f"{backend_url}/api/core/traces/?trace_id={trace_id}")
            if response.status_code != 200:
                return {'error': 'Trace not found'}
            
            traces = response.json()
            if not traces:
                return {'error': 'Trace not found'}
            
            trace = traces[0]
            
            # Get spans
            spans_response = client.get(f"{backend_url}/api/core/spans/?trace={trace['id']}")
            spans = spans_response.json() if spans_response.status_code == 200 else []
            
            # Calculate total duration
            if spans:
                start_times = [span['start_time'] for span in spans if span.get('start_time')]
                end_times = [span['end_time'] for span in spans if span.get('end_time')]
                
                if start_times and end_times:
                    # Update trace with calculated duration
                    earliest = min(start_times)
                    latest = max(end_times)
                    
                    return {
                        'trace_id': trace_id,
                        'span_count': len(spans),
                        'start': earliest,
                        'end': latest
                    }
            
            return {'trace_id': trace_id, 'span_count': len(spans)}
    except Exception as e:
        logger.error(f"Error correlating trace {trace_id}: {e}")
        return {'error': str(e)}


@celery_task
def evaluate_alert_rules(metric: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate metric against active alert rules.
    """
    import httpx
    
    backend_url = os.getenv('BACKEND_URL', 'http://backend:8000')
    alerts_triggered = []
    
    try:
        # Fetch active alert rules
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                f"{backend_url}/api/notification/rules/",
                params={'is_active': True, 'metric_name': metric.get('name')}
            )
            rules = response.json() if response.status_code == 200 else []
        
        for rule in rules:
            threshold = rule.get('threshold', 0)
            operator = rule.get('operator', 'gt')
            value = metric.get('value', 0)
            
            triggered = False
            if operator == 'gt' and value > threshold:
                triggered = True
            elif operator == 'gte' and value >= threshold:
                triggered = True
            elif operator == 'lt' and value < threshold:
                triggered = True
            elif operator == 'lte' and value <= threshold:
                triggered = True
            elif operator == 'eq' and value == threshold:
                triggered = True
            
            if triggered:
                alerts_triggered.append({
                    'rule_id': rule.get('id'),
                    'rule_name': rule.get('name'),
                    'metric_name': metric.get('name'),
                    'metric_value': value,
                    'threshold': threshold
                })
        
        return {'alerts_triggered': len(alerts_triggered), 'details': alerts_triggered}
    except Exception as e:
        logger.error(f"Error evaluating alert rules: {e}")
        return {'error': str(e)}


@celery_task
def run_anomaly_detection(metric_name: str, window_minutes: int = 60) -> Dict[str, Any]:
    """
    Run anomaly detection on metric time series.
    Uses simple statistical methods (mean ± 3*std).
    """
    import httpx
    import statistics
    
    backend_url = os.getenv('BACKEND_URL', 'http://backend:8000')
    
    try:
        since = (datetime.now(timezone.utc) - timedelta(minutes=window_minutes)).isoformat()
        
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{backend_url}/api/core/metrics/",
                params={'name': metric_name, 'timestamp__gte': since}
            )
            metrics = response.json() if response.status_code == 200 else []
        
        if len(metrics) < 10:
            return {'status': 'insufficient_data', 'count': len(metrics)}
        
        values = [m.get('value', 0) for m in metrics]
        mean = statistics.mean(values)
        stdev = statistics.stdev(values)
        
        lower_bound = mean - (3 * stdev)
        upper_bound = mean + (3 * stdev)
        
        anomalies = [
            m for m in metrics 
            if m.get('value', 0) < lower_bound or m.get('value', 0) > upper_bound
        ]
        
        return {
            'metric_name': metric_name,
            'window_minutes': window_minutes,
            'data_points': len(metrics),
            'mean': mean,
            'stdev': stdev,
            'anomalies_detected': len(anomalies),
            'anomaly_ids': [a.get('id') for a in anomalies[:10]]
        }
    except Exception as e:
        logger.error(f"Error running anomaly detection: {e}")
        return {'error': str(e)}
