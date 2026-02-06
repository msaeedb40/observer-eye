"""Performance Router - Performance monitoring and optimization."""
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import httpx

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

router = APIRouter()


class PerformanceMetric(BaseModel):
    """Performance metric model."""
    name: str
    value: float
    unit: str
    timestamp: datetime
    source: Optional[str] = None
    labels: Optional[dict] = None


@router.get("/metrics")
async def get_performance_metrics(
    source: Optional[str] = None,
    limit: int = Query(default=100, le=1000)
):
    """Get performance metrics from backend."""
    try:
        async with httpx.AsyncClient() as client:
            params = {"source": source, "limit": limit}
            resp = await client.get(f"{BACKEND_URL}/api/v1/performance/metrics/", params=params)
            if resp.status_code == 200:
                return resp.json().get('results', [])
            return []
    except Exception:
        return []


@router.post("/metrics")
async def record_performance_metric(metric: PerformanceMetric):
    """Record a performance metric via backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BACKEND_URL}/api/v1/performance/metrics/", json=metric.model_dump())
            return resp.json()
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@router.get("/summary")
async def get_performance_summary():
    """Get performance summary from backend aggregate views."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/performance/summary/")
            if resp.status_code == 200:
                return resp.json()
            return {
                "average_response_time": 0.0,
                "p95_response_time": 0.0,
                "p99_response_time": 0.0,
                "total_requests": 0,
                "error_rate": 0.0
            }
    except Exception:
        return {
            "average_response_time": 0.0,
            "p95_response_time": 0.0,
            "p99_response_time": 0.0,
            "total_requests": 0,
            "error_rate": 0.0
        }
