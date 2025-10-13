import os
from dotenv import load_dotenv
import requests
from typing import Any, Optional

# Load .env variables
load_dotenv()

CUSTOMERS_API = os.getenv("CUSTOMERS_API")
PRODUCTS_API = os.getenv("PRODUCTS_API")
SALES_API = os.getenv("SALES_API")
FISCAL_API = os.getenv("FISCAL_API")
INTEGRATED_API = os.getenv("INTEGRATED_API")

def extract_customers() -> Optional[Any]:
    """Fetch customers from the API."""
    try:
        response = requests.get(CUSTOMERS_API)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch customers: {e}")
        return None

def extract_products() -> Optional[Any]:
    """Fetch products from the API."""
    try:
        response = requests.get(PRODUCTS_API)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch products: {e}")
        return None

def extract_sales() -> Optional[Any]:
    """Fetch sales from the API."""
    try:
        response = requests.get(SALES_API)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch sales: {e}")
        return None
    
def extract_fiscal_movements() -> Optional[Any]:
    """Fetch fiscal movements from the API."""
    try:
        response = requests.get(FISCAL_API)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch fiscal movements: {e}")
        return None

def extract_integrated_movements() -> Optional[Any]:
    """Fetch integrated movements from the API."""
    try:
        response = requests.get(INTEGRATED_API)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch integrated movements: {e}")
        return None