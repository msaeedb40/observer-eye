import requests

BASE_URL = "http://localhost:8000"
ANOMALIES_ENDPOINT = "/api/v1/insights/anomalies/"
TIMEOUT = 30

def test_list_detected_anomalies_and_validate_output():
    url = BASE_URL + ANOMALIES_ENDPOINT
    headers = {
        "Accept": "application/json",
    }
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        # Validate HTTP response status
        assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"

        # Validate JSON response content type header
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Expected JSON response but got Content-Type: {content_type}"

        data = response.json()
        # The response should be a list or dict containing anomalies
        assert isinstance(data, (list, dict)), f"Expected response type list or dict but got {type(data)}"

        # If list, check each anomaly object has expected keys and types
        anomalies = data if isinstance(data, list) else data.get("anomalies", data)
        assert anomalies is not None, "Response missing expected anomalies data"

        if isinstance(anomalies, list):
            for anomaly in anomalies:
                assert isinstance(anomaly, dict), "Each anomaly entry should be a dictionary"
                # Check typical anomaly fields if present
                # Example common fields: id, timestamp, metric_name, severity, description
                # We validate that at least these fields exist if anomalies list is non-empty
                if anomaly:
                    for field in ["id", "timestamp", "metric_name", "severity", "description"]:
                        assert field in anomaly, f"Anomaly object missing expected field '{field}'"
        else:
            # If not a list, we may expect a dictionary with anomaly details or summary
            assert isinstance(anomalies, dict), "Expected anomalies data to be dict if not list"

    except requests.exceptions.RequestException as e:
        assert False, f"Request failed: {e}"

test_list_detected_anomalies_and_validate_output()