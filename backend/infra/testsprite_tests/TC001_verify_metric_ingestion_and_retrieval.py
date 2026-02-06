import requests

BASE_URL = "http://localhost:8000"
METRICS_ENDPOINT = "/api/v1/core/metrics/"
TIMEOUT = 30
HEADERS = {"Content-Type": "application/json"}

INVALID_STRINGS = [' nominal', 'sample', 'placeholder', ' synthetic']

def assert_no_invalid_strings_in_metrics(metrics):
    for metric in metrics:
        for key, value in metric.items():
            if isinstance(value, str):
                for invalid_str in INVALID_STRINGS:
                    assert invalid_str not in value, f"Found invalid string '{invalid_str}' in metric {key}: {value}"

def test_verify_metric_ingestion_and_retrieval():
    # Step 1: Retrieve metrics initially and confirm it's empty or fresh (no invalid strings)
    try:
        resp_get_initial = requests.get(
            BASE_URL + METRICS_ENDPOINT, timeout=TIMEOUT, headers=HEADERS
        )
        assert resp_get_initial.status_code == 200, \
            f"Initial GET metrics failed with status code {resp_get_initial.status_code}"
        initial_response = resp_get_initial.json()
        if isinstance(initial_response, dict) and 'results' in initial_response:
            initial_metrics = initial_response['results']
        else:
            initial_metrics = initial_response
        assert isinstance(initial_metrics, list), f"Expected list of metrics, got {type(initial_metrics)}"
        # It should be empty or contain no invalid strings if there is fresh data
        assert_no_invalid_strings_in_metrics(initial_metrics)

        # Step 2: Ingest a new metric via POST
        metric_to_post = {
            "name": "cpu_usage_test",
            "source": "unit_test_suite",
            "value": 55.5,
            "timestamp": "2026-02-06T12:00:00Z"
        }

        resp_post = requests.post(
            BASE_URL + METRICS_ENDPOINT, json=metric_to_post, timeout=TIMEOUT, headers=HEADERS
        )
        assert resp_post.status_code in (200, 201), \
            f"POST metric failed with status code {resp_post.status_code}, response: {resp_post.text}"

        # Step 3: Retrieve metrics filtered by name and source
        params = {"name": metric_to_post["name"], "source": metric_to_post["source"]}
        resp_get_filtered = requests.get(
            BASE_URL + METRICS_ENDPOINT, params=params, timeout=TIMEOUT, headers=HEADERS
        )
        assert resp_get_filtered.status_code == 200, \
            f"Filtered GET metrics failed with status code {resp_get_filtered.status_code}"
        filtered_response = resp_get_filtered.json()
        if isinstance(filtered_response, dict) and 'results' in filtered_response:
            filtered_metrics = filtered_response['results']
        else:
            filtered_metrics = filtered_response
        assert isinstance(filtered_metrics, list), f"Expected list, got {type(filtered_metrics)}"
        assert len(filtered_metrics) > 0, "Filtered metrics list is empty after ingestion"

        # Step 4: Validate that all filtered metrics contain no invalid strings
        assert_no_invalid_strings_in_metrics(filtered_metrics)

        # Step 5: Validate the posted metric appears in the filtered results
        matching_metrics = [
            m for m in filtered_metrics
            if m.get("name") == metric_to_post["name"] and m.get("source") == metric_to_post["source"]
        ]
        assert matching_metrics, "Ingested metric not found in filtered results"

    finally:
        # Clean up: Attempt to delete ingested metric if API supports DELETE (not documented here)
        # If no DELETE, no cleanup possible through API, so skip.
        pass

test_verify_metric_ingestion_and_retrieval()