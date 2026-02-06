import requests

BASE_URL = "http://localhost:8000"
LOGS_ENDPOINT = f"{BASE_URL}/api/v1/core/logs/"
TIMEOUT = 30

def test_validate_log_listing_functionality():
    try:
        # Test retrieving logs without filters/pagination
        response = requests.get(LOGS_ENDPOINT, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        data = response.json()
        
        # Expecting a dict containing a list of logs under a key like 'results' or fallback to the root if list
        if isinstance(data, dict):
            if 'results' in data and isinstance(data['results'], list):
                logs = data['results']
            else:
                possible_keys = ['logs', 'items', 'data']
                logs = None
                for key in possible_keys:
                    if key in data and isinstance(data[key], list):
                        logs = data[key]
                        break
                assert logs is not None, "Response JSON dict does not contain a list of logs under expected keys"
        elif isinstance(data, list):
            logs = data
        else:
            assert False, "Expected response to be a list or dict containing list of logs"
        
        assert isinstance(logs, list), "Expected logs to be a list"

        if logs:
            sample_log = logs[0]
            assert isinstance(sample_log, dict), "Each log entry should be a dictionary"

    except requests.RequestException as e:
        assert False, f"RequestException occurred: {e}"
    except ValueError as e:
        assert False, f"Failed to decode JSON response: {e}"

test_validate_log_listing_functionality()
