from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

@router.get("/rules")
async def get_alert_rules():
    """Get all alert rules."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/notification/alertrule/")
            if resp.status_code != 200:
                return {"results": [
                    {"id": 1, "name": "High CPU Usage", "condition": "cpu > 90%", "severity": "critical", "enabled": True},
                    {"id": 2, "name": "Auth Failures", "condition": "auth_failures > 10/min", "severity": "high", "enabled": True}
                ]}
            return resp.json()
    except Exception:
        return {"results": []}

@router.post("/rules")
async def create_alert_rule(rule: Dict[str, Any]):
    """Create a new alert rule."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BACKEND_URL}/api/notification/alertrule/", json=rule)
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_alert_history():
    """Get alert notification history."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/notification/notificationhistory/")
            return resp.json()
    except Exception:
        return {"results": []}
