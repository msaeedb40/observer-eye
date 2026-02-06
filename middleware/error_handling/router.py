"""Error Handling Router - Error handling and recovery."""
import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ErrorLog(BaseModel):
    name: str
    message: str
    stack: Optional[str] = None
    level: str = "error"
    source: str = "frontend"
    timestamp: datetime = datetime.now()

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

@router.get("/logs")
async def get_error_logs(
    severity: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = 100
):
    """Get error logs from backend core logs."""
    try:
        async with httpx.AsyncClient() as client:
            params = {"limit": limit}
            if severity: params["level"] = severity
            if source: params["source"] = source
            
            resp = await client.get(f"{BACKEND_URL}/api/v1/core/logs/", params=params)
            if resp.status_code != 200:
                return {"errors": []}
            return {"errors": resp.json().get('results', []), "filters": {"severity": severity, "source": source}}
    except Exception:
        return {"errors": [], "filters": {"severity": severity, "source": source}}

@router.post("/logs")
async def record_error(error: ErrorLog):
    """Record an error in backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BACKEND_URL}/api/v1/core/logs/", json=error.model_dump())
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_error_stats():
    """Get error statistics from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/core/logs/summary/")
            if resp.status_code != 200:
                return {"total_errors": 0}
            return resp.json()
    except Exception:
        return {"total_errors": 0}
