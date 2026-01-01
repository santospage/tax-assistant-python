import os
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from dotenv import load_dotenv
load_dotenv()

LOGIN_API = os.getenv("LOGIN_API")
API_USER = os.getenv("API_USER")
API_PASSWORD = os.getenv("API_PASSWORD")
SSL_CERT_PATH = os.getenv("SSL_CERT_PATH", "src/certs/server-cert.pem")

_cached_token = None

def get_ssl_verify():
    """Return SSL certificate path if available, otherwise disable verification."""
    #if SSL_CERT_PATH and os.path.exists(SSL_CERT_PATH):
        #return SSL_CERT_PATH
    return False

def get_jwt_token():
    """Authenticate and return JWT token, using cached token when possible."""
    global _cached_token

    if _cached_token:
        return _cached_token

    try:
        response = requests.post(
            LOGIN_API,
            json={"user": API_USER, "password": API_PASSWORD},            
            verify=get_ssl_verify(),
        )
        response.raise_for_status()
        data = response.json()

        token = data.get("token") or data.get("access_token")
        if token:
            _cached_token = token
            return token

        print("Token not found in login response.")
        return None

    except requests.RequestException as e:
        print(f"Failed to authenticate at {LOGIN_API}: {e}")
        return None
