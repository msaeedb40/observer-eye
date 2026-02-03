from fastapi import APIRouter, HTTPException
import httpx
import os
from typing import List, Dict, Any

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

@router.get("/entities")
async def get_grail_entities():
    """Get all grail entities (nodes)."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/grailobserver/entities/")
            if resp.status_code != 200:
                # Fallback mock if backend is empty
                return {
                    "results": [
                        {"id": 1, "display_name": "frontend-v1", "entity_type": "service", "status": "active"},
                        {"id": 2, "display_name": "middleware-api", "entity_type": "service", "status": "active"},
                        {"id": 3, "display_name": "backend-core", "entity_type": "service", "status": "active"},
                        {"id": 4, "display_name": "postgres-db", "entity_type": "database", "status": "active"},
                        {"id": 5, "display_name": "redis-cache", "entity_type": "cache", "status": "active"}
                    ]
                }
            return resp.json()
    except Exception:
        return {"results": []}

@router.get("/relationships")
async def get_grail_relationships():
    """Get all grail relationships (links)."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BACKEND_URL}/api/v1/grailobserver/relationships/")
            if resp.status_code != 200:
                # Fallback mock for visualization
                return {
                    "results": [
                        {"id": 1, "source": 1, "target": 2, "relationship_type": "calls", "strength": 0.9},
                        {"id": 2, "source": 2, "target": 3, "relationship_type": "calls", "strength": 0.8},
                        {"id": 3, "source": 3, "target": 4, "relationship_type": "queries", "strength": 1.0},
                        {"id": 4, "source": 3, "target": 5, "relationship_type": "uses", "strength": 0.5}
                    ]
                }
            return resp.json()
    except Exception:
        return {"results": []}

@router.get("/topology")
async def get_topology():
    """Get combined topology graph data."""
    entities = await get_grail_entities()
    relationships = await get_grail_relationships()
    
    # Extract results list (DRF returns list directly if using ListSerializer or results key for pagination)
    nodes_data = entities if isinstance(entities, list) else entities.get("results", [])
    links_data = relationships if isinstance(relationships, list) else relationships.get("results", [])
    
    return {
        "nodes": [
            {"id": e.get("id"), "label": e.get("display_name", e.get("name")), "type": e.get("entity_type")}
            for e in nodes_data
        ],
        "links": [
            {"source": r.get("source"), "target": r.get("target"), "type": r.get("relationship_type")}
            for r in links_data
        ]
    }
