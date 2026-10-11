import pytest
import pandas as pd
import numpy as np
from app.services.analytics import (
    calculate_portfolio_returns,
    calculate_volatility,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
    calculate_risk_contributions
)
from app.services.risk_engine import classify_portfolio_risk
from app.services.allocation_engine import generate_recommended_allocation

@pytest.fixture
def sample_price_data():
    """Generates synthetic price data for testing calculations."""
    dates = pd.date_range(start="2023-01-01", periods=100, freq="B")
    np.random.seed(42)
    
    prices_a = 100 * (1 + np.random.normal(0.001, 0.01, 100)).cumprod()
    prices_b = 50 * (1 + np.random.normal(0.002, 0.025, 100)).cumprod()
    prices_c = 10 * (1 + np.random.normal(0.0003, 0.003, 100)).cumprod()
    
    return pd.DataFrame({
        "AAPL": prices_a,
        "TSLA": prices_b,
        "BND": prices_c
    }, index=dates)

def test_calculate_portfolio_returns(sample_price_data):
    weights = {"AAPL": 0.4, "TSLA": 0.4, "BND": 0.2}
    daily_returns, cum_returns = calculate_portfolio_returns(sample_price_data, weights)
    
    assert isinstance(daily_returns, pd.Series)
    assert len(daily_returns) == len(sample_price_data) - 1
    assert not cum_returns.empty

def test_calculate_volatility(sample_price_data):
    weights = {"AAPL": 0.5, "TSLA": 0.5, "BND": 0.0}
    daily_returns, _ = calculate_portfolio_returns(sample_price_data, weights)
    ann_vol = calculate_volatility(daily_returns)
    
    assert isinstance(ann_vol, float)
    assert ann_vol > 0.0

def test_calculate_max_drawdown(sample_price_data):
    weights = {"AAPL": 0.33, "TSLA": 0.33, "BND": 0.34}
    _, cum_returns = calculate_portfolio_returns(sample_price_data, weights)
    mdd = calculate_max_drawdown(cum_returns)
    
    assert isinstance(mdd, float)
    assert 0.0 <= mdd <= 1.0

def test_calculate_sharpe_ratio(sample_price_data):
    weights = {"AAPL": 0.5, "TSLA": 0.5, "BND": 0.0}
    daily_returns, _ = calculate_portfolio_returns(sample_price_data, weights)
    ann_vol = calculate_volatility(daily_returns)
    sharpe = calculate_sharpe_ratio(daily_returns, ann_vol, risk_free_rate=0.02)
    
    assert isinstance(sharpe, float)

def test_calculate_risk_contributions(sample_price_data):
    weights = {"AAPL": 0.5, "TSLA": 0.3, "BND": 0.2}
    risk_contribs = calculate_risk_contributions(sample_price_data, weights)
    
    assert "AAPL" in risk_contribs
    assert "TSLA" in risk_contribs
    assert "BND" in risk_contribs
    assert pytest.approx(sum(risk_contribs.values()), 0.01) == 1.0

def test_risk_classification():
    low_risk = classify_portfolio_risk(volatility=0.08, max_drawdown=0.05, asset_count=5)
    assert low_risk["risk_level"] == "Low"
    
    high_risk = classify_portfolio_risk(volatility=0.35, max_drawdown=0.40, asset_count=1)
    assert high_risk["risk_level"] == "High"

def test_generate_recommended_allocation():
    current_weights = {"AAPL": 0.7, "TSLA": 0.3}
    rec_low = generate_recommended_allocation(current_weights, target_risk="Low")
    
    assert pytest.approx(sum(rec_low.values()), 0.01) == 1.0
    assert len(rec_low) == len(current_weights)
