from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

@router.get("/metrics")
async def get_traffic_metrics():
    """Get Layer 7 traffic performance metrics from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/traffic-perf/performance/")
            if resp.status_code != 200:
                return {
                    "requests_per_second": 0.0,
                    "avg_response_size_kb": 0.0,
                    "http_5xx_rate": 0.0,
                    "top_endpoints": []
                }
            return resp.json().get('results', resp.json())
    except Exception:
        return {"error": "traffic metrics unavailable"}

@router.get("/analysis")
async def get_traffic_analysis():
    """Get detailed traffic bottleneck analysis from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/traffic-perf/analysis/")
            if resp.status_code != 200:
                return {"bottlenecks": []}
            return resp.json().get('results', resp.json())
    except Exception:
        return {"bottlenecks": []}
