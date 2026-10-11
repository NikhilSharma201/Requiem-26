import pytest
from app.services.risk_engine import classify_portfolio_risk

def test_risk_engine_low_risk():
    res = classify_portfolio_risk(volatility=0.08, max_drawdown=0.05, asset_count=5)
    assert res["risk_level"] == "Low"
    assert res["risk_score"] < 35.0
    assert "explanation" in res
    assert "metrics_summary" in res

def test_risk_engine_medium_risk():
    res = classify_portfolio_risk(volatility=0.20, max_drawdown=0.18, asset_count=3)
    assert res["risk_level"] in ["Low", "Medium"]
    assert 0.0 <= res["risk_score"] <= 100.0

def test_risk_engine_high_risk():
    res = classify_portfolio_risk(volatility=0.40, max_drawdown=0.35, asset_count=1)
    assert res["risk_level"] == "High"
    assert res["risk_score"] >= 70.0
