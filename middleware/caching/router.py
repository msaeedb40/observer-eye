"""Caching Router - Redis-backed caching layer implementation."""
import os
import json
import redis.asyncio as redis
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict

router = APIRouter()

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
_redis_client = None


def get_redis():
    """Get or create Redis client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client


class CacheEntry(BaseModel):
    """Cache entry model."""
    key: str
    value: Any
    ttl: Optional[int] = 3600  # Default 1 hour


@router.get("/get/{key}")
async def get_cached_value(key: str):
    """Get a cached value from Redis."""
    r = await get_redis()
    value = await r.get(key)
    
    if value:
        try:
            return {"key": key, "value": json.loads(value), "exists": True}
        except Exception:
            return {"key": key, "value": value, "exists": True}
    
    return {"key": key, "value": None, "exists": False}


@router.post("/set")
async def set_cached_value(entry: CacheEntry):
    """Set a cached value in Redis."""
    r = await get_redis()
    value_str = json.dumps(entry.value) if not isinstance(entry.value, str) else entry.value
    await r.set(entry.key, value_str, ex=entry.ttl)
    return {"status": "cached", "key": entry.key, "ttl": entry.ttl}


@router.delete("/delete/{key}")
async def delete_cached_value(key: str):
    """Delete a cached value from Redis."""
    r = await get_redis()
    await r.delete(key)
    return {"status": "deleted", "key": key}


@router.post("/invalidate")
async def invalidate_cache(pattern: Optional[str] = "*"):
    """Invalidate cache entries matching pattern."""
    r = await get_redis()
    keys = await r.keys(pattern)
    if keys:
        await r.delete(*keys)
    return {"status": "invalidated", "pattern": pattern, "count": len(keys) if keys else 0}


@router.get("/stats")
async def get_cache_stats():
    """Get Redis statistics."""
    r = await get_redis()
    info = await r.info()
    return {
        "hits": info.get('keyspace_hits', 0),
        "misses": info.get('keyspace_misses', 0),
        "hit_rate": float(info.get('keyspace_hits', 0)) / (float(info.get('keyspace_hits', 0)) + float(info.get('keyspace_misses', 1))) if (info.get('keyspace_hits', 0) + info.get('keyspace_misses', 0)) > 0 else 0.0,
        "total_keys": info.get('db0', {}).get('keys', 0),
        "memory_usage": f"{info.get('used_memory_human', '0B')}"
    }
