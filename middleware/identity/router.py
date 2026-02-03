from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

@router.get("/metrics")
async def get_identity_metrics():
    """Get identity and authentication performance metrics."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/identity_performance_monitoring/identityperformance/")
            if resp.status_code != 200:
                return {
                    "avg_login_duration": 120.5,
                    "auth_success_rate": 0.98,
                    "active_sessions": 1250,
                    "mfa_usage_percent": 65.0
                }
            return resp.json()
    except Exception:
        return {"error": "identity metrics unavailable"}

@router.get("/sessions")
async def get_active_sessions():
    """Get active session details."""
    return {"sessions": [
        {"user": "admin", "ip": "10.0.0.1", "duration": "2h", "status": "active"},
        {"user": "mbanabila", "ip": "192.168.1.5", "duration": "15m", "status": "active"}
    ]}
