# tests/test_extract.py
import src.etl.extract as extract_data_from_api

try:
    import responses  # type: ignore
except ImportError as e:
    raise ImportError("Missing dependency 'responses'. Install with: pip install responses") from e

from src.etl.extract import extract_data_from_api

@responses.activate
def test_extract_data_from_api_pagination():
    base_url = "https://localhost:8443/api/customers"
    responses.add(
        responses.GET,
        f"{base_url}?page=0&size=50",
        json={"content": [{"id": 1, "name": "Customer1"}]},
        status=200,
    )
    responses.add(
        responses.GET,
        f"{base_url}?page=1&size=50",
        json={"content": []},
        status=200,
    )

    headers = {"Authorization": "Bearer fake-token"}
    data = extract_data_from_api(base_url, headers, verify_setting=False)
    assert len(data) == 1
    assert data[0]["name"] == "Customer1"
