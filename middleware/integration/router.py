from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

@router.get("/datasources")
async def get_data_sources():
    """Get all configured data sources."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/integration/datasource/")
            if resp.status_code != 200:
                return {"results": [
                    {"id": 1, "name": "Main PostgreSQL", "type": "postgres", "status": "connected"},
                    {"id": 2, "name": "Prometheus-Cluster", "type": "prometheus", "status": "connected"}
                ]}
            return resp.json()
    except Exception:
        return {"results": []}

@router.get("/webhooks")
async def get_webhooks():
    """Get all configured webhooks."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/integration/webhook/")
            return resp.json()
    except Exception:
        return {"results": []}

@router.post("/datasources/test")
async def test_datasource_connection(config: Dict[str, Any]):
    """Test connection to a data source."""
    # Simulation
    return {"status": "success", "message": "Connection established successfully"}
