from fastapi import APIRouter, HTTPException
import httpx
import os
import random
import uuid
from typing import List, Dict, Any
from datetime import datetime, timedelta

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

@router.get("/forecast")
async def get_forecast(metric: str = "cpu_usage"):
    """Get predictive metric forecast from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/insights/insights/forecast/?metric={metric}")
            if resp.status_code == 200:
                return resp.json()
            # Fallback if backend fails or not implemented
            return {"metric": metric, "forecast": [], "error": "Backend prediction unavailable"}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@router.get("/correlation")
async def get_cross_domain_correlation():
    """Identify correlations from backend analysis."""
    # Currently backend doesn't have a direct correlation endpoint, so we might need to 
    # fetch anomalies and correlate them manually or keep this as future work.
    # For now, we'll return a placeholder or fetch anomalies to show "potential" correlations.
    try:
        async with httpx.AsyncClient() as client:
             resp = await client.get(f"{BACKEND_URL}/api/v1/insights/anomalies/?limit=10")
             if resp.status_code != 200:
                 return {"correlations": []}
             
             anomalies = resp.json().get('results', [])
             # Simple logic: multiple anomalies in short time = correlation
             if len(anomalies) > 2:
                 return {
                     "correlations": [{
                         "domains": list(set(a['source'] for a in anomalies)),
                         "factor": 0.8,
                         "insight": f"Multiple anomalies detected across {len(anomalies)} sources."
                     }]
                 }
             return {"correlations": []}
    except Exception as e:
        return {"correlations": [], "error": str(e)}

@router.get("/root-cause")
async def get_root_cause(trace_id: str = None):
    """Trigger AI root cause analysis on backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BACKEND_URL}/api/v1/insights/insights/analyze_root_cause/",
                json={"incident_id": trace_id or str(uuid.uuid4())}
            )
            if resp.status_code == 200:
                return resp.json()
            raise HTTPException(status_code=resp.status_code, detail="Backend analysis failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
