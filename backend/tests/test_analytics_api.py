import pytest
from unittest.mock import patch
import pandas as pd
import numpy as np

@pytest.fixture
def mock_batch_prices():
    dates = pd.date_range(start="2023-01-01", periods=100, freq="B")
    np.random.seed(42)
    prices_a = 100 * (1 + np.random.normal(0.001, 0.01, 100)).cumprod()
    prices_b = 50 * (1 + np.random.normal(0.002, 0.02, 100)).cumprod()
    bench = 400 * (1 + np.random.normal(0.0005, 0.008, 100)).cumprod()
    
    return pd.DataFrame({
        "AAPL": prices_a,
        "MSFT": prices_b,
        "^GSPC": bench
    }, index=dates)

def test_evaluate_portfolio_api_success(client, mock_batch_prices):
    with patch("app.routers.analytics.get_batch_historical_prices", return_value=mock_batch_prices):
        payload = {
            "allocations": {"AAPL": 0.6, "MSFT": 0.4},
            "target_risk": "Low",
            "benchmark": "^GSPC"
        }
        response = client.post("/analytics/evaluate", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["risk_level"] in ["Low", "Medium", "High"]
        assert "annualized_volatility" in data
        assert "ai_market_intelligence" in data

def test_evaluate_portfolio_invalid_allocation_sum(client):
    payload = {
        "allocations": {"AAPL": 0.5, "MSFT": 0.1},
        "target_risk": "Low"
    }
    response = client.post("/analytics/evaluate", json=payload)
    assert response.status_code == 400
    assert "Allocations must sum to 1.0" in response.json()["detail"]
