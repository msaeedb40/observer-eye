import requests
import uuid

BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json"
}
TIMEOUT = 30

def test_manage_dashboard_templates_import_export():
    # Sample dashboard template data to create/import
    template_payload = {
        "name": f"Test Template {uuid.uuid4()}",
        "description": "A test dashboard template created for TC006",
        "widgets": [
            {
                "type": "chart",
                "title": "Sample Chart",
                "config": {
                    "metric": "cpu_usage",
                    "chart_type": "line",
                    "time_range": "last_24_hours"
                }
            }
        ]
    }

    created_template_id = None

    try:
        # Step 1: Create/Import a dashboard template
        create_response = requests.post(
            f"{BASE_URL}/api/v1/dashboards/templates/",
            json=template_payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert create_response.status_code == 201, f"Expected 201 Created, got {create_response.status_code}"
        create_response_json = create_response.json()
        assert "id" in create_response_json, "Response JSON must contain 'id'"
        created_template_id = create_response_json["id"]
        assert create_response_json.get("name") == template_payload["name"], "Template name mismatch on creation"

        # Step 2: List dashboard templates and verify created template exists
        list_response = requests.get(
            f"{BASE_URL}/api/v1/dashboards/templates/",
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert list_response.status_code == 200, f"Expected 200 OK from list, got {list_response.status_code}"
        templates_response = list_response.json()
        # Handle if templates are paginated or direct list
        if isinstance(templates_response, dict):
            # Common pattern: {'count': n, 'results': [...]} or similar
            templates = templates_response.get('results', [])
        else:
            templates = templates_response
        assert isinstance(templates, list), "Expected list of templates"

        # Find the created template by ID in the list
        found_template = next((t for t in templates if t.get("id") == created_template_id), None)
        assert found_template is not None, "Created template not found in template listing"
        assert found_template.get("name") == template_payload["name"], "Template name mismatch in listing"
        assert found_template.get("description") == template_payload["description"], "Template description mismatch in listing"

    finally:
        # Cleanup: delete the created template if exists
        if created_template_id:
            try:
                delete_response = requests.delete(
                    f"{BASE_URL}/api/v1/dashboards/templates/{created_template_id}/",
                    headers=HEADERS,
                    timeout=TIMEOUT
                )
                # Accepting 204 No Content or 200 OK as successful delete
                assert delete_response.status_code in (200, 204), f"Failed to delete template with id {created_template_id}"
            except Exception:
                pass

test_manage_dashboard_templates_import_export()
