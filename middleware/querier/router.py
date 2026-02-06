"""
Querier Router for Observer-Eye Middleware.
Provides endpoints for PromQL and instant queries.
"""
from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from typing import Optional, List
from .promql_engine import PromQLEngine

router = APIRouter()
engine = PromQLEngine()

@router.get("/query")
async def instant_query(
    query: str = Query(..., description="PromQL query expression"),
    time: Optional[datetime] = Query(None, description="Evaluation timestamp")
):
    """Execute instant query at a specific point in time."""
    try:
        results = await engine.execute_instant(query, time)
        return {
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": results
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/query_range")
async def range_query(
    query: str = Query(..., description="PromQL query expression"),
    start: datetime = Query(..., description="Start timestamp"),
    end: datetime = Query(..., description="End timestamp"),
    step: str = Query("1m", description="Query resolution step width")
):
    """Execute range query over a time window."""
    try:
        results = await engine.execute_range(query, start, end, step)
        return {
            "status": "success",
            "data": {
                "resultType": "matrix",
                "result": results
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metadata")
async def get_metadata(metric: Optional[str] = None):
    """Get metric metadata from the backend."""
    import httpx
    import os
    
    backend_url = os.getenv("BACKEND_URL", "http://backend:8000")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{backend_url}/api/v1/core/metrics/metadata/",
                params={"metric": metric}
            )
            
            if resp.status_code == 200:
                return resp.json()
            else:
                return {
                    "status": "success",
                    "data": {metric: [{"type": "gauge", "help": "No metadata available"}]} if metric else {}
                }
    except Exception:
        # Graceful fallback if metadata endpoint doesn't exist yet
        return {
            "status": "success",
            "data": {metric: [{"type": "gauge", "help": f"Metadata for {metric}"}]} if metric else {}
        }
