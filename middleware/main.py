"""
Observer-Eye Middleware - FastAPI Application

Logic Layer for Observer-Eye Observability Platform
Port: 8400

4 Pillars of Observability: Metrics, Events, Logs, Traces
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"level": "%(levelname)s", "time": "%(asctime)s", "module": "%(module)s", "message": "%(message)s"}'
)
logger = logging.getLogger("observer_eye_middleware")


# =============================================================================
# APPLICATION LIFESPAN
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Observer-Eye Middleware starting up...")
    yield
    logger.info("Observer-Eye Middleware shutting down...")


# =============================================================================
# APPLICATION INSTANCE
# =============================================================================

app = FastAPI(
    title="Observer-Eye Middleware",
    description="Logic Layer for Observer-Eye Observability Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# =============================================================================
# CORS CONFIGURATION
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:80,http://localhost:4200,http://localhost:3000"
    ).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# TELEMETRY MIDDLEWARE
# =============================================================================

@app.middleware("http")
async def telemetry_middleware(request: Request, call_next):
    """Add telemetry tracking to all requests."""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Add request ID to headers
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Add observability headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log request (Logs pillar)
    logger.info(f"Request: {request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
    
    return response


# =============================================================================
# HEALTH CHECK ENDPOINTS
# =============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "observer-eye-middleware",
        "version": "1.0.0"
    }


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Readiness check endpoint."""
    return {
        "status": "ready",
        "backend_connected": True,
        "cache_connected": True
    }


# =============================================================================
# API ROUTERS
# =============================================================================

# Import and include routers
from performance.router import router as performance_router
from error_handling.router import router as error_handling_router
from caching.router import router as caching_router
from streaming.router import router as streaming_router
from data_processing.router import router as data_processing_router
from analytics.router import router as analytics_router
from netmetrics.router import router as netmetrics_router
from systemmetrics.router import router as systemmetrics_router
from security.router import router as security_router
from insights.router import router as insights_router
from grail.router import router as grail_router
from notification.router import router as notification_router
from integration.router import router as integration_router
from identity.router import router as identity_router
from traffic.router import router as traffic_router
from testing.router import router as testing_router

# Include routers with prefixes
app.include_router(performance_router, prefix="/api/v1/performance", tags=["Performance"])
app.include_router(error_handling_router, prefix="/api/v1/errors", tags=["Error Handling"])
app.include_router(caching_router, prefix="/api/v1/cache", tags=["Caching"])
app.include_router(streaming_router, prefix="/api/v1/stream", tags=["Streaming"])
app.include_router(data_processing_router, prefix="/api/v1/data", tags=["Data Processing"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(netmetrics_router, prefix="/api/v1/network", tags=["Network Metrics"])
app.include_router(systemmetrics_router, prefix="/api/v1/system", tags=["System Metrics"])
app.include_router(security_router, prefix="/api/v1/security", tags=["Security"])
app.include_router(insights_router, prefix="/api/v1/insights", tags=["AI Insights"])
app.include_router(grail_router, prefix="/api/v1/grail", tags=["Grail Observer"])
app.include_router(notification_router, prefix="/api/v1/notifications", tags=["Notifications & Alerts"])
app.include_router(integration_router, prefix="/api/v1/integrations", tags=["Integrations"])
app.include_router(identity_router, prefix="/api/v1/identity", tags=["Identity Performance"])
app.include_router(traffic_router, prefix="/api/v1/traffic", tags=["Traffic Performance"])
app.include_router(testing_router, prefix="/api/v1/testing", tags=["Testing"])


# =============================================================================
# BACKEND PROXY ENDPOINTS (Forward to Django)
# =============================================================================

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

@app.api_route("/api/v1/backend/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_to_backend(path: str, request: Request):
    """Proxy requests to the Django backend with data processing."""
    import httpx
    
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}/api/v1/{path}"
        
        # Forward request to backend
        response = await client.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers.items() if key.lower() != 'host'},
            content=await request.body() if request.method in ["POST", "PUT", "PATCH"] else None,
            params=dict(request.query_params)
        )
        
        return JSONResponse(
            content=response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text},
            status_code=response.status_code,
            headers={"X-Proxied-From": "backend"}
        )


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if os.environ.get("DEBUG", "false").lower() == "true" else "An unexpected error occurred",
            "request_id": request.headers.get("X-Request-ID", "unknown")
        }
    )


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8400,
        reload=True,
        log_level="info"
    )
