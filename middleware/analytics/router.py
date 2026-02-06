from fastapi import APIRouter, HTTPException, Query
import httpx
import os
from typing import Dict, Any, List, Optional
import statistics
from .anomaly_detection import AnomalyDetector

router = APIRouter()
detector = AnomalyDetector()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

@router.get("/health-score")
async def get_health_score():
    """Calculate overall system health score based on metrics and error rates."""
    try:
        async with httpx.AsyncClient() as client:
            # Fetch recent metrics and events
            metrics_resp = await client.get(f"{BACKEND_URL}/api/v1/core/metrics/?limit=100")
            events_resp = await client.get(f"{BACKEND_URL}/api/v1/core/events/?limit=50")
            
            if metrics_resp.status_code != 200 or events_resp.status_code != 200:
                return {"score": 0, "status": "unknown", "note": "Backend data unavailable"}

            metrics = metrics_resp.json().get('results', [])
            events = events_resp.json().get('results', [])
            
            # Simple heuristic
            score = 100
            
            # Deduct for critical events
            critical_events = [e for e in events if e.get('severity') == 'critical']
            score -= len(critical_events) * 10
            
            # Deduct for errors
            error_events = [e for e in events if e.get('severity') == 'error']
            score -= len(error_events) * 5
            
            # Check for high CPU/Memory in metrics
            high_usage = [m for m in metrics if 'usage' in m.get('name', '') and m.get('value', 0) > 90]
            score -= len(high_usage) * 2
            
            if score > 80:
                status = "healthy"
            elif score > 50:
                status = "degraded"
            else:
                status = "unhealthy"

            return {
                "score": score,
                "status": status,
                "breakdown": {
                    "critical_events": len(critical_events),
                    "error_events": len(error_events),
                    "resource_warnings": len(high_usage)
                }
            }
    except Exception as e:
        return {"score": 100, "status": "unknown", "error": str(e)}

@router.get("/metrics/aggregate")
async def aggregate_metrics(name: str = Query(...)):
    """Aggregate metric values for a specific name."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/core/metrics/?name={name}&limit=100")
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail="Failed to fetch from backend")
                
            data = resp.json().get('results', [])
            if not data:
                return {"name": name, "avg": 0, "count": 0}
                
            values = [m['value'] for m in data]
            return {
                "name": name,
                "avg": statistics.mean(values),
                "max": max(values),
                "min": min(values),
                "count": len(values),
                "last_value": values[0] if values else 0
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/anomalies")
async def detect_anomalies(name: str = Query(...), threshold: float = 3.0):
    """Detect anomalies in a specific metric."""
    try:
        detector.threshold = threshold
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/core/metrics/?name={name}&limit=200")
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail="Failed to fetch from backend")
                
            data = resp.json().get('results', [])
            if not data:
                return {"name": name, "anomalies": []}
                
            # Prepare data for detector
            series = [{"timestamp": m['timestamp'], "value": m['value']} for m in data]
            results = detector.detect_anomalies_series(series)
            
            anomalies = [r for r in results if r['is_anomaly']]
            
            return {
                "name": name,
                "total_points": len(series),
                "anomaly_count": len(anomalies),
                "anomalies": anomalies,
                "latest_score": results[0]['anomaly_score'] if results else 0
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
