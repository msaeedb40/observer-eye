from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

@router.get("/summary")
async def get_network_summary():
    """Get summarized network metrics."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/netmetrics/networkmetric/?limit=50")
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail="Backend unavailable")
            
            data = resp.json().get('results', [])
            return {
                "total_sent_bytes": sum(m.get('bytes_sent', 0) for m in data),
                "total_received_bytes": sum(m.get('bytes_received', 0) for m in data),
                "avg_latency_ms": sum(m.get('latency_ms', 0) for m in data) / len(data) if data else 0,
                "hosts_monitored": len(set(m.get('host') for m in data))
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/connections")
async def get_active_connections():
    """Get active connection counts per host."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/netmetrics/connectionmetric/?limit=10")
            if resp.status_code != 200:
                return {"active": 0, "hosts": []}
            return resp.json()
    except Exception:
        return {"error": "connection metrics unavailable"}
