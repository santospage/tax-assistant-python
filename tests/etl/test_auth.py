# tests/test_auth.py
from unittest.mock import Mock
import requests
from src import auth

def test_get_jwt_token_success(monkeypatch):
    login_api = "https://localhost:8443/api/auth/login"
    monkeypatch.setenv("LOGIN_API", login_api)
    monkeypatch.setenv("API_USER", "admin")
    monkeypatch.setenv("API_PASSWORD", "123456")

    # create a fake response object for requests.post
    mock_resp = Mock()
    mock_resp.json.return_value = {"token": "mocked-jwt-token"}
    mock_resp.status_code = 200

    # patch requests.post to return the fake response
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: mock_resp)

    token = auth.get_jwt_token()
    assert token == "mocked-jwt-token"
