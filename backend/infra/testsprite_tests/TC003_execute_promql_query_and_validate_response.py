import requests
import time

BASE_URL = "http://localhost:8000"
TIMEOUT = 30
HEADERS = {
    "Content-Type": "application/json",
    # Add authentication headers here if needed, e.g.
    # "Authorization": "Bearer <token>"
}

def test_execute_promql_query_and_validate_response():
    url = f"{BASE_URL}/api/v1/queriers/execute/"

    # Valid PromQL-like query payload
    valid_payload = {
        "query": "rate(http_requests_total[5m])",
        "time_range": "now-5m"
    }

    # Invalid PromQL-like query payload (malformed query)
    invalid_payload = {
        "query": "rate(http_requests_total[5min",  # missing closing bracket
        "time_range": "now-5m"
    }

    # Test valid query
    start_time = time.time()
    try:
        valid_response = requests.post(url, json=valid_payload, headers=HEADERS, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Valid query request failed: {e}"
    duration = time.time() - start_time

    assert valid_response.status_code == 200, f"Expected status 200 for valid query but got {valid_response.status_code}"
    try:
        valid_json = valid_response.json()
    except ValueError:
        assert False, "Valid query response is not valid JSON"

    # Validate presence of expected fields in the response, common PromQL responses contain "data" or "result"
    assert isinstance(valid_json, dict), "Valid query response JSON is not a dict"
    assert "data" in valid_json or "result" in valid_json or "results" in valid_json, \
        "Valid query response JSON missing expected fields (data/result/results)"
    # Validate performance: response within 5 seconds (example)
    assert duration <= 5, f"Query execution took too long: {duration:.2f}s"

    # Test invalid query
    try:
        invalid_response = requests.post(url, json=invalid_payload, headers=HEADERS, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Invalid query request failed: {e}"

    # Expected: error response with 4xx status code
    assert invalid_response.status_code >= 400 and invalid_response.status_code < 500, \
        f"Expected client error status for invalid query but got {invalid_response.status_code}"
    try:
        invalid_json = invalid_response.json()
    except ValueError:
        # Some APIs might return plain text error, so allowance here
        invalid_json = None

    if invalid_json:
        # Check presence of error information
        error_fields = ["error", "message", "detail"]
        assert any(field in invalid_json for field in error_fields), \
            "Invalid query error response missing error details"

test_execute_promql_query_and_validate_response()