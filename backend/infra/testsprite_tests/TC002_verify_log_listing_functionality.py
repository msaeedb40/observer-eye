import requests

BASE_URL = "http://localhost:8000"
LOGS_ENDPOINT = f"{BASE_URL}/api/v1/core/logs/"
TIMEOUT = 30

def test_verify_log_listing_functionality():
    forbidden_substrings = [' nominal', 'sample', 'placeholder', ' synthetic']
    try:
        response = requests.get(LOGS_ENDPOINT, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"GET {LOGS_ENDPOINT} failed with exception: {e}"

    data = response.json()
    # Check that data is a list or dict containing logs
    # logs could be list or could be nested - we assume data is the top-level logs structure
    # Since no schema is defined for the logs response, we verify none of the fields contain forbidden substrings.

    # Collect all string values recursively from the response json
    def gather_strings(element):
        strings = []
        if isinstance(element, dict):
            for v in element.values():
                strings.extend(gather_strings(v))
        elif isinstance(element, list):
            for item in element:
                strings.extend(gather_strings(item))
        elif isinstance(element, str):
            strings.append(element)
        return strings

    all_strings = gather_strings(data)
    for forbidden in forbidden_substrings:
        for s in all_strings:
            assert forbidden not in s, f"Found forbidden substring '{forbidden}' in log data: '{s}'"

    # Check that metrics list is initially empty or reflects fresh data since platform was purged
    # From the PRD, metrics list is presumably separate, but instruction says verify metrics list empty or fresh.
    # We'll query metrics to verify that:

    metrics_endpoint = f"{BASE_URL}/api/v1/core/metrics/"
    try:
        metrics_response = requests.get(metrics_endpoint, timeout=TIMEOUT)
        metrics_response.raise_for_status()
    except requests.RequestException as e:
        assert False, f"GET {metrics_endpoint} failed with exception: {e}"

    metrics_data = metrics_response.json()
    # According to PRD, fetching metrics returns a list or dict - we consider it returns list of metrics
    # We verify list is empty or reasonably empty (fresh platform)
    if isinstance(metrics_data, list):
        assert len(metrics_data) == 0, f"Expected metrics list to be empty after purge, found {len(metrics_data)} metrics."
    elif isinstance(metrics_data, dict):
        # maybe it has a 'results' or 'metrics' key, check presence of metrics
        possible_keys = ['results', 'metrics', 'data']
        found_metrics = None
        for key in possible_keys:
            if key in metrics_data:
                found_metrics = metrics_data[key]
                break
        if found_metrics is None:
            # No recognized keys holding metrics, assume empty
            pass
        else:
            if isinstance(found_metrics, list):
                assert len(found_metrics) == 0, f"Expected metrics list to be empty after purge, found {len(found_metrics)} metrics."
            else:
                # If it's not a list, just check truthy vs falsy
                assert not found_metrics, f"Expected metrics list to be empty after purge, found non-empty data."
    else:
        # Unrecognized format, fail
        assert False, f"Unexpected metrics data format: {type(metrics_data)}"

test_verify_log_listing_functionality()