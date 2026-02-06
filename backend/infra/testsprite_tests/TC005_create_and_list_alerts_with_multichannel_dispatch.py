import requests
import time

BASE_URL = "http://localhost:8000"
ALERTS_ENDPOINT = f"{BASE_URL}/api/v1/notification/alerts/"
HEADERS = {
    "Content-Type": "application/json"
}
TIMEOUT = 30

def test_create_and_list_alerts_with_multichannel_dispatch():
    alert_payload = {
        "name": "High CPU Usage Alert",
        "description": "Alert for high CPU usage",
        "severity": "high",
        "enabled": True,
        "conditions": [
            {
                "type": "metric_threshold",
                "metric": "cpu_usage",
                "threshold": 90,
                "operator": ">"
            }
        ],
        "channels": [
            {
                "type": "email",
                "config": {
                    "recipient": "alerts@example.com",
                    "subject": "High CPU Usage Alert"
                }
            },
            {
                "type": "slack",
                "config": {
                    "channel": "#alerts",
                    "message": "CPU usage is above 90%"
                }
            }
        ]
    }

    created_alert_id = None

    try:
        # Create alert via POST
        create_resp = requests.post(ALERTS_ENDPOINT, json=alert_payload, headers=HEADERS, timeout=TIMEOUT)
        assert create_resp.status_code == 201, f"Expected status 201 Created, got {create_resp.status_code}"
        create_resp_json = create_resp.json()
        assert "id" in create_resp_json, "Response JSON missing 'id'"
        created_alert_id = create_resp_json["id"]

        # Wait briefly to ensure alert dispatch process (if async) can occur
        time.sleep(2)

        # Retrieve alerts list via GET
        list_resp = requests.get(ALERTS_ENDPOINT, headers=HEADERS, timeout=TIMEOUT)
        assert list_resp.status_code == 200, f"Expected status 200 OK, got {list_resp.status_code}"
        alerts_list_json = list_resp.json()

        # Adjust to get alerts list from key 'results' if present, else expect whole json is list
        if isinstance(alerts_list_json, dict) and "results" in alerts_list_json:
            alerts_list = alerts_list_json["results"]
        else:
            alerts_list = alerts_list_json

        assert isinstance(alerts_list, list), "Alerts list response is not a list"

        # Check that created alert is in the list
        alert_found = False
        for alert in alerts_list:
            if alert.get("id") == created_alert_id:
                alert_found = True
                # Validate key fields match creation payload
                assert alert.get("name") == alert_payload["name"], "Alert name mismatch"
                assert alert.get("description") == alert_payload["description"], "Alert description mismatch"
                assert alert.get("severity") == alert_payload["severity"], "Alert severity mismatch"
                assert alert.get("enabled") == alert_payload["enabled"], "Alert enabled state mismatch"
                # Validate channels exist and match types specified
                channels = alert.get("channels")
                assert isinstance(channels, list), "Alert channels is not a list or missing"
                channel_types = []
                for ch in channels:
                    if isinstance(ch, dict) and "type" in ch and isinstance(ch["type"], str):
                        channel_types.append(ch["type"])
                for ch_required in ["email", "slack"]:
                    assert ch_required in channel_types, f"Alert channel '{ch_required}' not found in alert channels"
                break

        assert alert_found, "Created alert not found in alerts list"

    finally:
        # Cleanup: delete the created alert if exists
        if created_alert_id:
            delete_resp = requests.delete(f"{ALERTS_ENDPOINT}{created_alert_id}/", headers=HEADERS, timeout=TIMEOUT)
            assert delete_resp.status_code in (200, 204), f"Expected status 200 or 204 on delete, got {delete_resp.status_code}"


test_create_and_list_alerts_with_multichannel_dispatch()
