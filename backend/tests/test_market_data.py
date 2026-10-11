import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.services import market_data

def test_get_current_price_returns_latest_close():
    mock_ticker = MagicMock()
    dates = pd.date_range("2024-01-01", periods=1)
    mock_ticker.history.return_value = pd.DataFrame({"Close": [150.0]}, index=dates)
    mock_ticker.fast_info = {"lastPrice": 150.0}

    with patch("app.services.market_data.yf.Ticker", return_value=mock_ticker):
        price = market_data.get_current_price("AAPL")
        assert price == 150.0

def test_get_current_price_raises_on_invalid_ticker():
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = pd.DataFrame()
    mock_ticker.fast_info = {}

    with patch("app.services.market_data.yf.Ticker", return_value=mock_ticker):
        with pytest.raises(HTTPException) as exc_info:
            market_data.get_current_price("INVALIDTICKER")
        assert exc_info.value.status_code == 404

def test_fetch_historical_data_returns_structured_list():
    dates = pd.date_range("2024-01-01", periods=3)
    mock_batch_df = pd.DataFrame({
        "AAPL": [100.0, 102.0, 101.0]
    }, index=dates)

    with patch("app.services.market_data.get_batch_historical_prices", return_value=mock_batch_df):
        result = market_data.fetch_historical_data("AAPL", period="3d")

    assert not result.empty
    assert len(result) == 3
    assert result.iloc[0]["close_price"] == 100.0

def test_fetch_historical_data_raises_on_empty_response():
    with patch("app.services.market_data.get_batch_historical_prices", return_value=pd.DataFrame()):
        result = market_data.fetch_historical_data("INVALIDTICKER")
        assert result.empty
