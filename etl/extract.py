import os
import json
import requests
from etl.auth import get_jwt_token, get_ssl_verify

# API endpoints from environment variables
CUSTOMERS_API = os.getenv("CUSTOMERS_API")
PRODUCTS_API = os.getenv("PRODUCTS_API")
SALES_API = os.getenv("SALES_API")
FISCAL_API = os.getenv("FISCAL_API")
INTEGRATED_API = os.getenv("INTEGRATED_API")

DATA_PATH = "data/raw"
PAGE_SIZE = 50


def fetch_api_data(api_url, output_filename):
    """Fetch paginated data from an API and save it to a local JSON file."""
    os.makedirs(DATA_PATH, exist_ok=True)
    all_data = []
    page = 0

    token = get_jwt_token()
    if not token:
        print(f"❌ Could not obtain JWT token. Skipping {api_url}")
        return

    headers = {"Authorization": f"Bearer {token}"}
    verify_setting = False

    def _fetch_page(url, hdrs, verify, pg):
        resp = requests.get(
            f"{url}?page={pg}&size={PAGE_SIZE}",
            headers=hdrs,
            verify=verify,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data
        return data.get("content", data)

    def _save(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    while True:
        try:
            page_data = _fetch_page(api_url, headers, verify_setting, page)

            if not page_data:
                break

            if not isinstance(page_data, list):
                page_data = [page_data]

            all_data.extend(page_data)
            print(f"✅ Page {page} extracted ({len(page_data)} items)")

            # Stop when last page is reached
            if len(page_data) < PAGE_SIZE:
                break

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"❌ HTTP/Network error fetching data from {api_url}: {e}")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            break

    output_path = os.path.join(DATA_PATH, output_filename)
    _save(output_path, all_data)
    print(f"💾 Saved {len(all_data)} records to {output_path}")

def extract_customers():
    fetch_api_data(CUSTOMERS_API, "customers.json")


def extract_products():
    fetch_api_data(PRODUCTS_API, "products.json")


def extract_sales():
    fetch_api_data(SALES_API, "sales_movements.json")


def extract_fiscal_movements():
    fetch_api_data(FISCAL_API, "fiscal_movements.json")


def extract_integrated_movements():
    fetch_api_data(INTEGRATED_API, "integrated_movements.json")
