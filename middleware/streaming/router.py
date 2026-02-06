"""Streaming Router - Real-time data streaming for observability data.

Provides WebSocket and SSE endpoints for:
- Live metrics streaming
- Real-time log tailing
- Event notifications
- Trace updates
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import StreamingResponse
from typing import List, Dict, Set, Optional
from enum import Enum
import asyncio
import json
import httpx
import os
from datetime import datetime, timezone
from caching.router import get_redis

router = APIRouter()

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")


class StreamChannel(str, Enum):
    """Available streaming channels."""
    METRICS = "metrics"
    LOGS = "logs"
    EVENTS = "events"
    TRACES = "traces"
    ALERTS = "alerts"
    ALL = "all"


class ConnectionManager:
    """
    Manages WebSocket connections with channel-based subscriptions.
    
    Clients can subscribe to specific channels (metrics, logs, events, traces, alerts)
    or to all channels at once.
    """
    
    def __init__(self):
        # Map of channel -> set of websockets
        self.channel_connections: Dict[StreamChannel, Set[WebSocket]] = {
            channel: set() for channel in StreamChannel
        }
        # Reverse mapping: websocket -> set of channels
        self.websocket_channels: Dict[WebSocket, Set[StreamChannel]] = {}
    
    async def connect(self, websocket: WebSocket, channels: List[StreamChannel] = None):
        """Accept a websocket connection and subscribe to specified channels."""
        await websocket.accept()
        
        if channels == None:
            channels = [StreamChannel.ALL]
        
        self.websocket_channels[websocket] = set(channels)
        
        for channel in channels:
            self.channel_connections[channel].add(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove a websocket from all subscribed channels."""
        channels = self.websocket_channels.pop(websocket, set())
        for channel in channels:
            self.channel_connections[channel].discard(websocket)
    
    def subscribe(self, websocket: WebSocket, channel: StreamChannel):
        """Add a channel subscription for an existing connection."""
        if websocket not in self.websocket_channels:
            return
        
        self.websocket_channels[websocket].add(channel)
        self.channel_connections[channel].add(websocket)
    
    def unsubscribe(self, websocket: WebSocket, channel: StreamChannel):
        """Remove a channel subscription for an existing connection."""
        if websocket not in self.websocket_channels:
            return
        
        self.websocket_channels[websocket].discard(channel)
        self.channel_connections[channel].discard(websocket)
    
    async def broadcast_to_channel(self, channel: StreamChannel, message: dict):
        """Broadcast a message to all connections subscribed to a channel."""
        message['channel'] = channel.value
        message['timestamp'] = datetime.now(timezone.utc).isoformat()
        
        # Send to channel subscribers
        for connection in self.channel_connections[channel].copy():
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)
        
        # Also send to 'all' subscribers
        if channel != StreamChannel.ALL:
            for connection in self.channel_connections[StreamChannel.ALL].copy():
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(connection)
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        message['timestamp'] = datetime.now(timezone.utc).isoformat()
        all_connections = set()
        for connections in self.channel_connections.values():
            all_connections.update(connections)
        
        for connection in all_connections.copy():
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)
    
    def get_stats(self) -> dict:
        """Get connection statistics."""
        return {
            "total_connections": len(self.websocket_channels),
            "channels": {
                channel.value: len(connections) 
                for channel, connections in self.channel_connections.items()
            }
        }
    
    async def listen_to_redis(self):
        """Background task to listen to Redis and broadcast to local websockets."""
        r = get_redis()
        pubsub = r.pubsub()
        await pubsub.subscribe(*[c.value for c in StreamChannel])
        
        logger.info(f"Redis Pub/Sub listener started for channels: {[c.value for c in StreamChannel]}")
        
        try:
            async for message in pubsub.listen():
                if message['type'] == 'message':
                    channel_name = message['channel']
                    try:
                        channel = StreamChannel(channel_name)
                        data = json.loads(message['data'])
                        await self.broadcast_to_channel(channel, data)
                    except Exception as e:
                        logger.error(f"Error processing Redis message: {e}")
        finally:
            await pubsub.unsubscribe()


manager = ConnectionManager()


# ========================
# WebSocket Endpoints
# ========================

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for real-time streaming.
    
    Clients can send subscription commands:
    - {"action": "subscribe", "channel": "metrics"}
    - {"action": "unsubscribe", "channel": "logs"}
    
    Receives data broadcasts for subscribed channels.
    """
    await manager.connect(websocket, [StreamChannel.ALL])
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                action = message.get('action')
                
                if action == 'subscribe':
                    channel_name = message.get('channel', 'all')
                    try:
                        channel = StreamChannel(channel_name)
                        manager.subscribe(websocket, channel)
                        await websocket.send_json({
                            "type": "subscribed",
                            "channel": channel_name
                        })
                    except ValueError:
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Unknown channel: {channel_name}"
                        })
                
                elif action == 'unsubscribe':
                    channel_name = message.get('channel', 'all')
                    try:
                        channel = StreamChannel(channel_name)
                        manager.unsubscribe(websocket, channel)
                        await websocket.send_json({
                            "type": "unsubscribed",
                            "channel": channel_name
                        })
                    except ValueError:
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Unknown channel for unsubscribe: {channel_name}"
                        })
                
                elif action == 'ping':
                    await websocket.send_json({"type": "pong"})
                
                else:
                    # Echo back unknown messages
                    await websocket.send_json({"type": "echo", "data": message})
                    
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/ws/{channel}")
async def channel_websocket(websocket: WebSocket, channel: str):
    """
    Channel-specific WebSocket endpoint.
    
    Connect directly to a specific channel:
    - /ws/metrics
    - /ws/logs
    - /ws/events
    - /ws/traces
    - /ws/alerts
    """
    try:
        stream_channel = StreamChannel(channel)
    except ValueError:
        await websocket.close(code=4004, reason=f"Unknown channel: {channel}")
        return
    
    await manager.connect(websocket, [stream_channel])
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get('action') == 'ping':
                    await websocket.send_json({"type": "pong"})
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON received on channel {channel}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ========================
# SSE (Server-Sent Events) Endpoints
# ========================

async def event_generator(channel: StreamChannel, request: Request):
    """Generate SSE events for a specific channel using Redis Pub/Sub."""
    r = get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(channel.value)
    
    try:
        async for message in pubsub.listen():
            if await request.is_disconnected():
                break
                
            if message['type'] == 'message':
                yield f"event: {channel.value}\ndata: {message['data']}\n\n"
    finally:
        await pubsub.unsubscribe()


@router.get("/sse/{channel}")
async def sse_endpoint(channel: str, request: Request):
    """
    Server-Sent Events endpoint for real-time streaming.
    
    Alternative to WebSocket for clients that prefer SSE:
    - /sse/metrics
    - /sse/logs
    - /sse/events
    - /sse/traces
    - /sse/alerts
    """
    try:
        stream_channel = StreamChannel(channel)
    except ValueError:
        return {"error": f"Unknown channel: {channel}"}
    
    return StreamingResponse(
        event_generator(stream_channel, request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


# ========================
# Management Endpoints
# ========================

@router.get("/connections")
async def get_active_connections():
    """Get WebSocket connection statistics."""
    return manager.get_stats()


@router.post("/broadcast")
async def broadcast_message(message: dict):
    """Broadcast a message to all connected clients."""
    await manager.broadcast(message)
    return {"status": "broadcasted", **manager.get_stats()}


@router.post("/broadcast/{channel}")
async def broadcast_to_channel(channel: str, message: dict):
    """Broadcast a message to a specific channel."""
    try:
        stream_channel = StreamChannel(channel)
    except ValueError:
        return {"error": f"Unknown channel: {channel}"}
    
    await manager.broadcast_to_channel(stream_channel, message)
    return {
        "status": "broadcasted",
        "channel": channel,
        "recipients": len(manager.channel_connections[stream_channel])
    }


@router.get("/channels")
async def list_channels():
    """List available streaming channels."""
    return {
        "channels": [
            {
                "name": channel.value,
                "description": f"Real-time {channel.value} stream",
                "connections": len(manager.channel_connections[channel])
            }
            for channel in StreamChannel
        ]
    }
