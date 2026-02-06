import requests
import uuid

BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json"
}
TIMEOUT = 30

def verify_alert_creation_and_listing():
    alert_create_url = f"{BASE_URL}/api/v1/notification/alerts/"
    alert_list_url = alert_create_url

    # Prepare alert payload with multiple channel dispatch configurations
    alert_payload = {
        "name": f"test-alert-{uuid.uuid4()}",
        "description": "Test alert for multi-channel dispatch verification",
        "severity": "critical",
        "enabled": True,
        "conditions": {
            "threshold": 90,
            "metric": "cpu_usage"
        },
        "dispatch_channels": [
            {"type": "email", "recipients": ["test@example.com"]},
            {"type": "slack", "channel": "#alerts"},
            {"type": "webhook", "url": "http://localhost:9000/webhook"}
        ]
    }

    alert_id = None
    try:
        # Create alert via POST
        create_resp = requests.post(alert_create_url, json=alert_payload, headers=HEADERS, timeout=TIMEOUT)
        assert create_resp.status_code == 201, f"Alert creation failed: {create_resp.text}"
        created_alert = create_resp.json()
        alert_id = created_alert.get("id")
        assert alert_id is not None and isinstance(alert_id, (int, str)), "Created alert ID missing or invalid"

        # Verify created alert fields do not contain hardcoded or mock strings
        forbidden_strings = [' nominal', 'sample', 'placeholder', ' synthetic']
        def check_forbidden_strings(obj):
            if isinstance(obj, dict):
                for v in obj.values():
                    check_forbidden_strings(v)
            elif isinstance(obj, list):
                for item in obj:
                    check_forbidden_strings(item)
            elif isinstance(obj, str):
                for forbidden in forbidden_strings:
                    assert forbidden not in obj, f"Forbidden string '{forbidden}' found in alert data"

        check_forbidden_strings(created_alert)

        # Retrieve alerts via GET
        list_resp = requests.get(alert_list_url, headers=HEADERS, timeout=TIMEOUT)
        assert list_resp.status_code == 200, f"Alert listing failed: {list_resp.text}"
        alert_list_resp = list_resp.json()

        # Adjusted to expect a dict response with a 'results' key listing alerts
        if isinstance(alert_list_resp, dict) and 'results' in alert_list_resp:
            alert_list = alert_list_resp['results']
        else:
            alert_list = alert_list_resp

        assert isinstance(alert_list, list), "Alert list response expected to be a list"

        # Verify none of the alerts contain forbidden strings
        for alert in alert_list:
            check_forbidden_strings(alert)

        # Verify metrics list is empty or fresh (no stale/hardcoded metrics)
        # Given platform just purged, metrics can be queried from /api/v1/core/metrics/
        metrics_resp = requests.get(f"{BASE_URL}/api/v1/core/metrics/", headers=HEADERS, timeout=TIMEOUT)
        assert metrics_resp.status_code == 200, f"Metrics listing failed: {metrics_resp.text}"
        metrics_resp_json = metrics_resp.json()

        # Adjusted to expect a dict response with 'results' key listing metrics
        if isinstance(metrics_resp_json, dict) and 'results' in metrics_resp_json:
            metrics = metrics_resp_json['results']
        else:
            metrics = metrics_resp_json

        assert isinstance(metrics, list), "Metrics response expected to be a list"

        # Check no metrics contain forbidden strings
        for metric in metrics:
            check_forbidden_strings(metric)

    finally:
        if alert_id:
            # Cleanup: delete the created alert after test
            delete_url = f"{alert_create_url}{alert_id}/"
            try:
                del_resp = requests.delete(delete_url, headers=HEADERS, timeout=TIMEOUT)
                # Accept 204 No Content or 200 OK for delete success
                assert del_resp.status_code in (200, 204), f"Alert deletion failed: {del_resp.text}"
            except Exception as e:
                # If deletion fails, log but do not fail test
                print(f"Warning: failed to delete alert {alert_id}: {e}")

verify_alert_creation_and_listing()
