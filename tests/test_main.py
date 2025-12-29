from unittest.mock import patch
from src.main import main

@patch("src.main.extract_integrated_movements")
@patch("src.main.extract_fiscal_movements")
@patch("src.main.extract_sales")
@patch("src.main.extract_products")
@patch("src.main.extract_customers")
def test_main_calls_extracts(
    mock_customers,
    mock_products,
    mock_sales,
    mock_fiscal,
    mock_integrated,
):
    main()

    mock_customers.assert_called_once()
    mock_products.assert_called_once()
    mock_sales.assert_called_once()
    mock_fiscal.assert_called_once()
    mock_integrated.assert_called_once()
