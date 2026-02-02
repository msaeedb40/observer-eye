"""Streaming Router - Real-time data streaming."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json

router = APIRouter()

# Connection manager for WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await manager.broadcast({"received": message})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get("/connections")
async def get_active_connections():
    """Get number of active WebSocket connections."""
    return {"active_connections": len(manager.active_connections)}


@router.post("/broadcast")
async def broadcast_message(message: dict):
    """Broadcast a message to all connected clients."""
    await manager.broadcast(message)
    return {"status": "broadcasted", "clients": len(manager.active_connections)}
