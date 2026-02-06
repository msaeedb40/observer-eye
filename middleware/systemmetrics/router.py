from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

@router.get("/summary")
async def get_system_summary():
    """Get summarized system metrics (CPU/Mem/Disk) from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/systemmetrics/system/?limit=10")
            if resp.status_code != 200:
                return {"avg_cpu_percent": 0, "avg_memory_percent": 0}
            
            data = resp.json().get('results', [])
            if not data:
                return {"avg_cpu_percent": 0, "avg_memory_percent": 0}
                
            return {
                "avg_cpu_percent": sum(m.get('cpu_percent', 0) for m in data) / len(data),
                "avg_memory_percent": sum(m.get('memory_percent', 0) for m in data) / len(data),
                "hosts": list(set(m.get('host') for m in data))
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
