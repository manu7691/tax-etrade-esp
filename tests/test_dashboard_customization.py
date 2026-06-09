import json
from unittest.mock import patch, MagicMock
from pathlib import Path
from generate_charts import load_ticker_config
from tax_engine.market_data import fetch_company_name

def test_load_ticker_config_txt(tmp_path):
    # Test loading from ticker.txt
    txt_file = tmp_path / "ticker.txt"
    txt_file.write_text("AAPL", encoding="utf-8")
    
    ticker, company_name = load_ticker_config(tmp_path)
    assert ticker == "AAPL"
    assert company_name is None

def test_load_ticker_config_json(tmp_path):
    # Test loading from ticker.json
    json_file = tmp_path / "ticker.json"
    json_file.write_text(json.dumps({"ticker": "DDOG", "company_name": "Datadog"}), encoding="utf-8")
    
    ticker, company_name = load_ticker_config(tmp_path)
    assert ticker == "DDOG"
    assert company_name == "Datadog"

def test_load_ticker_config_json_simple(tmp_path):
    # Test loading simple string from ticker.json
    json_file = tmp_path / "ticker.json"
    json_file.write_text(json.dumps("ESTC"), encoding="utf-8")
    
    ticker, company_name = load_ticker_config(tmp_path)
    assert ticker == "ESTC"
    assert company_name is None

@patch("requests.get")
def test_fetch_company_name_api(mock_get):
    # Mock search API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "quotes": [
            {"longname": "Datadog, Inc.", "shortname": "Datadog", "symbol": "DDOG"}
        ]
    }
    mock_get.return_value = mock_response
    
    name = fetch_company_name("DDOG")
    assert name == "Datadog, Inc."
    mock_get.assert_called_once_with(
        "https://query1.finance.yahoo.com/v1/finance/search?q=DDOG&quotesCount=1",
        headers={'User-Agent': 'Mozilla/5.0'},
        timeout=5
    )
