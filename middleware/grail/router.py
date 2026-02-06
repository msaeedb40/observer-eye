from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

@router.get("/entities")
async def get_grail_entities():
    """Get all grail entities (nodes) from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/grailobserver/entities/")
            if resp.status_code != 200:
                return {"results": []}
            return resp.json().get('results', [])
    except Exception:
        return {"results": []}

@router.get("/relationships")
async def get_grail_relationships():
    """Get all grail relationships (links) from backend."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/grailobserver/relationships/")
            if resp.status_code != 200:
                return {"results": []}
            return resp.json().get('results', [])
    except Exception:
        return {"results": []}

@router.get("/topology")
async def get_topology():
    """Get combined topology graph data formatted for D3."""
    entities_data = await get_grail_entities()
    relationships_data = await get_grail_relationships()
    
    # Ensure we are working with lists
    nodes_data = entities_data if isinstance(entities_data, list) else entities_data.get("results", [])
    links_data = relationships_data if isinstance(relationships_data, list) else relationships_data.get("results", [])
    
    # Format for TopologyNode interface
    nodes = [
        {
            "id": e.get("entity_id", str(e.get("id"))),
            "name": e.get("display_name"),
            "type": e.get("entity_type"),
            "status": e.get("health_status", "unknown").replace("degraded", "warning").replace("unhealthy", "critical")
        }
        for e in nodes_data
    ]
    
    # Format for TopologyLink interface
    links = []
    for r in links_data:
        source = r.get("source")
        target = r.get("target")
        
        if isinstance(source, dict):
            source = source.get("entity_id", str(source.get("id")))
        if isinstance(target, dict):
            target = target.get("entity_id", str(target.get("id")))
            
        links.append({
            "source": source,
            "target": target,
            "type": r.get("relationship_type"),
            "status": "healthy"
        })
    
    return {
        "nodes": nodes,
        "links": links
    }
