from src.etl import (
    extract_customers,
    extract_products,
    extract_sales,
    extract_fiscal_movements,
    extract_integrated_movements,
)

def main():
    print("🚀 Starting ETL pipeline...")

    extract_customers()
    extract_products()
    extract_sales()
    extract_fiscal_movements()
    extract_integrated_movements()

    print("✅ ETL process completed successfully!")

if __name__ == "__main__":
    main()
