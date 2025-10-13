from etl.extract import extract_customers, extract_products, extract_sales

def main():
    """
    Main ETL pipeline entry point.
    Orchestrates extraction of data from multiple APIs.
    """
    # Extract data from APIs
    customers = extract_customers()
    products = extract_products()
    sales = extract_sales()

    # Print results (placeholder for further transformation and loading)
    print("Customers:", customers)
    print("Products:", products)
    print("Sales:", sales)


# Standard Python idiom for script entry
if __name__ == "__main__":
    main()
