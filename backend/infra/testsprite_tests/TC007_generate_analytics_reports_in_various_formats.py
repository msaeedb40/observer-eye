import requests

BASE_URL = "http://localhost:8000"
ENDPOINT = "/api/v1/analytics/reports/generate/"
TIMEOUT = 30

def test_generate_analytics_reports_in_various_formats():
    url = BASE_URL + ENDPOINT
    headers = {"Content-Type": "application/json"}
    report_types = ["summary", "detailed", "trend"]  # Assuming common report types to test
    formats = ["PDF", "CSV"]

    for rtype in report_types:
        for rformat in formats:
            payload = {"type": rtype, "format": rformat}
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
                # Validate HTTP status
                assert response.status_code == 200, f"Failed for type {rtype} and format {rformat} with status {response.status_code}"
                # Validate content type header for returned report matches requested format
                content_type = response.headers.get("Content-Type", "")
                if rformat == "PDF":
                    assert "application/pdf" in content_type, f"Expected PDF content type but got {content_type}"
                elif rformat == "CSV":
                    assert "text/csv" in content_type, f"Expected CSV content type but got {content_type}"
                # Validate response content is not empty
                assert response.content and len(response.content) > 0, "Empty report content received"
            except (requests.RequestException, AssertionError) as e:
                raise AssertionError(f"Report generation failed for type '{rtype}' and format '{rformat}': {e}")

test_generate_analytics_reports_in_various_formats()