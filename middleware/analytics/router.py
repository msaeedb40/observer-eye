from fastapi import APIRouter, HTTPException, Query
import httpx
import os
from typing import Dict, Any, List
import statistics

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

@router.get("/health-score")
async def get_health_score():
    """Calculate overall system health score based on metrics and error rates."""
    try:
        async with httpx.AsyncClient() as client:
            # Fetch recent metrics and events
            metrics_resp = await client.get(f"{BACKEND_URL}/api/core/metrics/?limit=100")
            events_resp = await client.get(f"{BACKEND_URL}/api/core/events/?limit=50")
            
            if metrics_resp.status_code != 200 or events_resp.status_code != 200:
                return {"score": 100, "status": "nominal (fallback)", "note": "Backend data unavailable"}

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
            
            score = max(0, min(100, score))
            
            return {
                "score": score,
                "status": "healthy" if score > 80 else "degraded" if score > 50 else "unhealthy",
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
            resp = await client.get(f"{BACKEND_URL}/api/core/metrics/?name={name}&limit=100")
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
