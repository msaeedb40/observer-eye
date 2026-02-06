"""Telemetry Router - Telemetry collection and forwarding."""
from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

router = APIRouter()


class Metric(BaseModel):
    """Metric data model (Metrics pillar)."""
    name: str
    value: float
    labels: Optional[Dict[str, str]] = None
    timestamp: Optional[datetime] = None


class Event(BaseModel):
    """Event data model (Events pillar)."""
    name: str
    data: Dict[str, Any]
    source: str
    timestamp: Optional[datetime] = None


class LogEntry(BaseModel):
    """Log entry model (Logs pillar)."""
    level: str
    message: str
    source: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None


class Span(BaseModel):
    """Trace span model (Traces pillar)."""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    attributes: Optional[Dict[str, Any]] = None


import httpx
import os
import logging
from .kafka_producer import get_kafka_producer
from .celery_tasks import (
    process_metrics_batch, 
    process_logs_batch, 
    process_traces_batch,
    CELERY_AVAILABLE
)
from fastapi import Response, status

logger = logging.getLogger(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def enrich_kubernetes_metadata(data: List[Dict[str, Any]], request_headers: Dict[str, str]):
    """
    Attempt to enrich telemetry data with Kubernetes metadata from request headers.
    Headers like 'X-K8s-Namespace', 'X-K8s-Pod-Name' are often added by sidecars/proxies.
    """
    k8s_namespace = request_headers.get('x-k8s-namespace')
    k8s_pod = request_headers.get('x-k8s-pod-name')
    k8s_node = request_headers.get('x-k8s-node-name')

    if k8s_namespace or k8s_pod or k8s_node:
        for item in data:
            labels = item.get('labels', {})
            if k8s_namespace: labels['k8s_namespace'] = k8s_namespace
            if k8s_pod: labels['k8s_pod_name'] = k8s_pod
            if k8s_node: labels['k8s_node_name'] = k8s_node
            item['labels'] = labels
            item['metadata'] = item.get('metadata', {})
            item['metadata'].update(labels)

async def ingest_data(topic: str, data: List[Dict], celery_task_func, request_headers: Dict[str, str] = None):
    """
    Unified async ingestion: Kafka (primary) -> Celery (fallback) -> Standard response.
    Returns 202 Accepted immediately.
    """
    if request_headers:
        enrich_kubernetes_metadata(data, request_headers)
    # 1. Try Kafka
    try:
        producer = await get_kafka_producer()
        if producer and producer.is_connected:
            if topic == 'metrics': await producer.send_metrics(data)
            elif topic == 'logs': await producer.send_logs(data)
            elif topic == 'traces': await producer.send_traces(data)
            elif topic == 'events': await producer.send_events(data)
            return {"status": "accepted", "ingestion": "kafka"}
    except Exception as e:
        logger.error(f"Kafka ingestion failed for {topic}: {e}")

    # 2. Fallback to Celery
    if CELERY_AVAILABLE:
        try:
            celery_task_func.delay(data)
            return {"status": "accepted", "ingestion": "celery"}
        except Exception as e:
            logger.error(f"Celery fallback failed for {topic}: {e}")

    return {"status": "error", "message": "All ingestion layers failed"}

# ========================
# METRICS PILLAR
# ========================

@router.post("/metrics", status_code=status.HTTP_202_ACCEPTED)
async def record_metrics(metrics: List[Metric], request: Request):
    """Record metrics asynchronously."""
    data = [m.model_dump() for m in metrics]
    return await ingest_data("metrics", data, process_metrics_batch, request.headers)


@router.get("/metrics")
async def get_metrics(name: Optional[str] = None):
    """Get metrics proxy."""
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}/api/v1/core/metrics/"
        params = {"name": name} if name else {}
        resp = await client.get(url, params=params)
        if resp.status_code != 200:
            return {"results": []}
        return resp.json().get('results', resp.json())


# ========================
# EVENTS PILLAR
# ========================

@router.post("/events", status_code=status.HTTP_202_ACCEPTED)
async def record_events(events: List[Event], request: Request):
    """Record events asynchronously."""
    data = [e.model_dump() for e in events]
    return await ingest_data("events", data, None, request.headers)


@router.get("/events")
async def get_events(source: Optional[str] = None):
    """Get events proxy."""
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}/api/v1/core/events/"
        params = {"source": source} if source else {}
        resp = await client.get(url, params=params)
        if resp.status_code != 200:
            return {"results": []}
        return resp.json().get('results', resp.json())


# ========================
# LOGS PILLAR
# ========================

@router.post("/logs", status_code=status.HTTP_202_ACCEPTED)
async def record_logs(logs: List[LogEntry], request: Request):
    """Record log entries asynchronously."""
    data = [l.model_dump() for l in logs]
    return await ingest_data("logs", data, process_logs_batch, request.headers)


@router.get("/logs")
async def get_logs(level: Optional[str] = None, source: Optional[str] = None):
    """Get log entries proxy from backend."""
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}/api/v1/core/logs/"
        params = {}
        if level: params['level'] = level
        if source: params['source'] = source
        resp = await client.get(url, params=params)
        if resp.status_code != 200:
            return {"results": []}
        return resp.json().get('results', resp.json())


# ========================
# TRACES PILLAR
# ========================

@router.post("/traces", status_code=status.HTTP_202_ACCEPTED)
async def record_traces(spans: List[Span], request: Request):
    """Record trace spans asynchronously."""
    data = [s.model_dump() for s in spans]
    return await ingest_data("traces", data, process_traces_batch, request.headers)


@router.get("/traces/{trace_id}")
async def get_trace(trace_id: str):
    """Get a complete trace from backend."""
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}/api/v1/core/traces/{trace_id}/"
        resp = await client.get(url)
        return resp.json()


@router.get("/traces")
async def list_traces(limit: int = 100):
    """List recent traces from backend."""
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}/api/v1/core/traces/"
        params = {"limit": limit}
        resp = await client.get(url, params=params)
        if resp.status_code != 200:
            return {"results": []}
        return resp.json().get('results', resp.json())
