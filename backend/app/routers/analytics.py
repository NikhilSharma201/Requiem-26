from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional, Any, List
import pandas as pd
import numpy as np

from app.services.market_data import get_batch_historical_prices
from app.services.analytics import (
    calculate_portfolio_returns,
    calculate_volatility,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
    calculate_risk_contributions
)
from app.services.risk_engine import classify_portfolio_risk
from app.services.allocation_engine import generate_recommended_allocation
from app.services.ai_intelligence import generate_ai_market_intelligence
from app.services.forecasting import forecast_portfolio_growth

router = APIRouter(prefix="/analytics", tags=["Analytics & Risk ML"])

class PortfolioAnalysisRequest(BaseModel):
    allocations: Dict[str, float] = Field(..., json_schema_extra={"example": {"AAPL": 0.5, "MSFT": 0.5}})
    target_risk: Optional[str] = Field("Medium", json_schema_extra={"example": "Low"})
    benchmark: Optional[str] = Field("^GSPC", json_schema_extra={"example": "^GSPC"})
    forecast_days: Optional[int] = Field(30, json_schema_extra={"example": 30})
    period: Optional[str] = Field("1y", json_schema_extra={"example": "1y"})

class RiskAnalysisResponse(BaseModel):
    risk_level: str
    risk_score: float
    explanation: str
    annualized_volatility: float
    max_drawdown: float
    sharpe_ratio: float
    total_period_return_pct: float
    risk_contributions: Dict[str, float]
    recommended_allocation: Dict[str, float]
    ai_market_intelligence: Dict[str, Any]
    historical_growth: List[Dict[str, Any]]
    asset_stats: Dict[str, Dict[str, float]]
    arima_forecast: Dict[str, Any]

@router.post("/evaluate", response_model=RiskAnalysisResponse)
def evaluate_portfolio(request: PortfolioAnalysisRequest):
    weights = {k.upper().strip(): v for k, v in request.allocations.items() if k.strip()}
    if not weights:
        raise HTTPException(status_code=400, detail="Allocations dict cannot be empty.")
    
    total_alloc = sum(weights.values())
    if not (0.99 <= total_alloc <= 1.01):
        raise HTTPException(status_code=400, detail="Allocations must sum to 1.0 (100%).")
        
    tickers = list(weights.keys())
    benchmark_symbol = (request.benchmark or "^GSPC").upper().strip()
    horizon = request.forecast_days or 30
    lookback_period = request.period or "1y"
    
    all_needed_tickers = tickers + [benchmark_symbol]
    
    price_df = get_batch_historical_prices(all_needed_tickers, period=lookback_period)
    
    if price_df.empty:
        raise HTTPException(status_code=400, detail="Failed to fetch real market data for requested tickers.")
        
    missing_assets = [t for t in tickers if t not in price_df.columns]
    if missing_assets:
        raise HTTPException(
            status_code=400, 
            detail=f"Could not retrieve historical price data for symbol(s): {', '.join(missing_assets)}"
        )
        
    portfolio_price_df = price_df[tickers]
    
    daily_returns, cum_returns = calculate_portfolio_returns(portfolio_price_df, weights)
    volatility = calculate_volatility(daily_returns)
    max_dd = calculate_max_drawdown(cum_returns)
    sharpe = calculate_sharpe_ratio(daily_returns, volatility)
    risk_contribs = calculate_risk_contributions(portfolio_price_df, weights)
    
    total_period_return = float(cum_returns.iloc[-1] * 100) if not cum_returns.empty else 0.0
    top_risk_asset = max(risk_contribs, key=risk_contribs.get) if risk_contribs else tickers[0]
    
    risk_ml = classify_portfolio_risk(
        volatility=volatility,
        max_drawdown=max_dd,
        asset_count=len(tickers)
    )
    
    recommended = generate_recommended_allocation(
        current_weights=weights,
        target_risk=request.target_risk or risk_ml["risk_level"]
    )

    ai_intel = generate_ai_market_intelligence(
        allocations=weights,
        risk_level=risk_ml["risk_level"],
        volatility=volatility,
        max_drawdown=max_dd,
        top_risk_asset=top_risk_asset
    )
    
    # 1. MULTI-STRATEGY HISTORICAL GROWTH PATHS
    returns_df = price_df.pct_change().dropna()
    
    user_w = pd.Series(weights)
    user_daily = returns_df[tickers].dot(user_w)
    
    rec_w = pd.Series(recommended)
    rec_daily = returns_df[tickers].dot(rec_w)
    
    eq_w = pd.Series({t: 1.0 / len(tickers) for t in tickers})
    eq_daily = returns_df[tickers].dot(eq_w)
    
    bench_col = benchmark_symbol if benchmark_symbol in returns_df.columns else returns_df.columns[0]
    bench_daily = returns_df[bench_col]

    cum_user = (1 + user_daily).cumprod()
    cum_rec = (1 + rec_daily).cumprod()
    cum_eq = (1 + eq_daily).cumprod()
    cum_bench = (1 + bench_daily).cumprod()

    growth_records = []
    for date_idx in returns_df.index:
        date_str = date_idx.strftime("%Y-%m-%d") if hasattr(date_idx, "strftime") else str(date_idx)
        growth_records.append({
            "date": date_str,
            "User Original Portfolio": float(round(cum_user.loc[date_idx], 4)),
            "ML Recommended Allocation": float(round(cum_rec.loc[date_idx], 4)),
            "Equal Weighted Portfolio": float(round(cum_eq.loc[date_idx], 4)),
            f"Benchmark ({benchmark_symbol})": float(round(cum_bench.loc[date_idx], 4))
        })

    # 2. INDIVIDUAL ASSET STATS
    asset_stats = {}
    for t in tickers:
        ann_ret = float(returns_df[t].mean() * 252 * 100)
        ann_vol = float(returns_df[t].std() * np.sqrt(252) * 100)
        asset_stats[t] = {
            "return_pct": round(ann_ret, 2),
            "volatility_pct": round(ann_vol, 2)
        }
        
    # 3. ARIMA FORECASTING
    arima_data = forecast_portfolio_growth(user_daily, forecast_days=horizon)
    
    return RiskAnalysisResponse(
        risk_level=risk_ml["risk_level"],
        risk_score=risk_ml["risk_score"],
        explanation=risk_ml["explanation"],
        annualized_volatility=round(volatility, 4),
        max_drawdown=round(max_dd, 4),
        sharpe_ratio=round(sharpe, 4),
        total_period_return_pct=round(total_period_return, 2),
        risk_contributions=risk_contribs,
        recommended_allocation=recommended,
        ai_market_intelligence=ai_intel,
        historical_growth=growth_records,
        asset_stats=asset_stats,
        arima_forecast=arima_data
    )
