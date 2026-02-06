from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

@router.get("/rules")
async def get_alert_rules():
    """Get all alert rules from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/notification/rules/")
            if resp.status_code != 200:
                return []
            data = resp.json()
            return data.get('results', data) if isinstance(data, dict) else data
    except Exception:
        return []

@router.post("/rules")
async def create_alert_rule(rule: Dict[str, Any]):
    """Create a new alert rule in backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BACKEND_URL}/api/v1/notification/rules/", json=rule)
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/rules/{rule_id}")
async def update_alert_rule(rule_id: int, rule: Dict[str, Any]):
    """Update an existing alert rule in backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.put(f"{BACKEND_URL}/api/v1/notification/rules/{rule_id}/", json=rule)
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/rules/{rule_id}")
async def delete_alert_rule(rule_id: int):
    """Delete an alert rule from backend."""
    try:
        async with httpx.AsyncClient() as client:
            await client.delete(f"{BACKEND_URL}/api/v1/notification/rules/{rule_id}/")
            return {"status": "deleted", "id": rule_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/channels")
async def get_notification_channels():
    """Get all notification channels from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/notification/channels/")
            if resp.status_code != 200:
                return []
            data = resp.json()
            return data.get('results', data) if isinstance(data, dict) else data
    except Exception:
        return []

@router.post("/channels")
async def create_notification_channel(channel: Dict[str, Any]):
    """Create a new notification channel in backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BACKEND_URL}/api/v1/notification/channels/", json=channel)
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/channels/{channel_id}")
async def update_notification_channel(channel_id: int, channel: Dict[str, Any]):
    """Update an existing notification channel in backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.put(f"{BACKEND_URL}/api/v1/notification/channels/{channel_id}/", json=channel)
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/channels/{channel_id}")
async def delete_notification_channel(channel_id: int):
    """Delete a notification channel from backend."""
    try:
        async with httpx.AsyncClient() as client:
            await client.delete(f"{BACKEND_URL}/api/v1/notification/channels/{channel_id}/")
            return {"status": "deleted", "id": channel_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_alert_history():
    """Get alert notification history from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/notification/history/")
            if resp.status_code != 200:
                return []
            data = resp.json()
            return data.get('results', data) if isinstance(data, dict) else data
    except Exception:
        return []

@router.get("/active")
async def get_active_alerts():
    """Get currently active alerts from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/notification/alerts/?status=active")
            if resp.status_code != 200:
                return []
            data = resp.json()
            return data.get('results', data) if isinstance(data, dict) else data
    except Exception:
        return []
