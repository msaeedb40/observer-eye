from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

@router.get("/threats")
async def get_security_threats():
    """Get recent security threat events."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/securitymetrics/threats/?limit=20")
            if resp.status_code != 200:
                return {"threats": []}
            return resp.json().get('results', [])
    except Exception:
        return {"error": "security data unavailable"}

@router.get("/stats")
async def get_security_stats():
    """Get security metrics summary."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/securitymetrics/security/?limit=10")
            if resp.status_code != 200:
                return {"auth_failures": 0}
            
            data = resp.json().get('results', [])
            return {
                "total_auth_attempts": sum(m.get('auth_attempts', 0) for m in data),
                "total_auth_failures": sum(m.get('auth_failures', 0) for m in data),
                "total_attacks_blocked": sum(m.get('blocked_requests', 0) for m in data)
            }
    except Exception:
        return {"error": "security stats unavailable"}
