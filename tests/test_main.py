# tests/test_main.py
from unittest.mock import patch
from src import main

@patch("src.main.get_jwt_token", return_value="mocked-token")
@patch("src.main.extract_data_from_api", return_value=[{"id": 1, "name": "Test"}])
def test_main_etl_success(mock_extract, mock_token, tmp_path):
    main.run_etl_pipeline()
    mock_token.assert_called_once()
    assert mock_extract.call_count > 0
