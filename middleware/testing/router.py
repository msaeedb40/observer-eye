import time
import httpx
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

router = APIRouter()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")


class TestCase(BaseModel):
    """Test case model."""
    name: str
    description: Optional[str] = None
    endpoint: str
    method: str = "GET"
    payload: Optional[Dict[str, Any]] = None
    expected_status: int = 200


class TestResult(BaseModel):
    """Test result model."""
    name: str
    passed: bool
    response_time: float
    status_code: int
    message: Optional[str] = None


async def _execute_test(test: TestCase) -> TestResult:
    """Internal helper to execute a test case."""
    start_time = time.time()
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = test.endpoint
            # If relative URL, assume it's for the backend proxy
            if not url.startswith("http"):
                url = f"{BACKEND_URL}/api/v1/{url.lstrip('/')}"
            
            response = await client.request(
                method=test.method,
                url=url,
                json=test.payload
            )
            
            passed = response.status_code == test.expected_status
            duration = time.time() - start_time
            
            return TestResult(
                name=test.name,
                passed=passed,
                response_time=duration,
                status_code=response.status_code,
                message=f"Expected {test.expected_status}, got {response.status_code}" if not passed else "Test passed"
            )
    except Exception as e:
        return TestResult(
            name=test.name,
            passed=False,
            response_time=time.time() - start_time,
            status_code=500,
            message=f"Error: {str(e)}"
        )


@router.post("/run", response_model=TestResult)
async def run_test_endpoint(test: TestCase):
    """Run a single test case against backend or external endpoints."""
    return await _execute_test(test)


@router.post("/run-suite")
async def run_test_suite_endpoint(tests: List[TestCase]):
    """Run multiple test cases sequentially."""
    results = []
    for test in tests:
        results.append(await _execute_test(test))
    
    passed_count = sum(1 for r in results if r.passed)
    return {
        "total": len(tests),
        "passed": passed_count,
        "failed": len(tests) - passed_count,
        "results": results,
        "execution_time": sum(r.response_time for r in results)
    }


@router.get("/health-check")
async def test_health_check():
    """Verify connectivity to core services."""
    start = time.time()
    backend_status = "unreachable"
    backend_time = 0.0
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            b_start = time.time()
            resp = await client.get(f"{BACKEND_URL}/health/") # Django health path
            backend_time = time.time() - b_start
            if resp.status_code == 200:
                backend_status = "healthy"
    except Exception:
        pass
        
    return {
        "overall_status": "healthy" if backend_status == "healthy" else "degraded",
        "services": {
            "backend": {"status": backend_status, "response_time": f"{backend_time:.4f}s"},
            "middleware": {"status": "healthy", "response_time": f"{time.time() - start:.4f}s"}
        }
    }
