import pytest
import pandas as pd
import numpy as np
from app.services.forecasting import forecast_portfolio_growth

def test_arima_forecasting_returns_forecast_dict():
    dates = pd.date_range(start="2023-01-01", periods=100, freq="B")
    np.random.seed(42)
    daily_returns = pd.Series(np.random.normal(0.001, 0.01, 100), index=dates)
    
    forecast_data = forecast_portfolio_growth(daily_returns, forecast_days=15)
    
    assert isinstance(forecast_data, dict)
    assert "historical_trail" in forecast_data
    assert "forecast" in forecast_data
    
    forecast_records = forecast_data["forecast"]
    assert len(forecast_records) == 16  # 1 start point + 15 forecast steps
    assert "date" in forecast_records[0]
    assert "forecast" in forecast_records[0]
    assert "lower_bound" in forecast_records[0]
    assert "upper_bound" in forecast_records[0]
    assert forecast_records[-1]["upper_bound"] >= forecast_records[-1]["lower_bound"]
