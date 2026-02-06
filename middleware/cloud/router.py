from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

@router.get("/metrics")
async def get_cloud_metrics():
    """Get summarized cloud resource metrics from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/cloud-perf/metrics/?limit=50")
            if resp.status_code != 200:
                return {"metrics": []}
            return resp.json().get('results', [])
    except Exception:
        return {"error": "cloud metrics unavailable"}

@router.get("/costs")
async def get_cloud_costs():
    """Get cloud cost monitoring data from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/cloud-perf/costs/?limit=20")
            if resp.status_code != 200:
                return {"costs": []}
            return resp.json().get('results', [])
    except Exception:
        return {"error": "cloud costs unavailable"}
