import numpy as np
import pandas as pd
from typing import Dict, Tuple

def calculate_portfolio_returns(
    price_df: pd.DataFrame, 
    weights: Dict[str, float]
) -> Tuple[pd.Series, pd.Series]:
    """Calculates weighted daily returns and cumulative portfolio growth."""
    asset_returns = price_df.pct_change().dropna()
    weight_series = pd.Series(weights)
    weight_series = weight_series / weight_series.sum()
    
    portfolio_daily_returns = asset_returns.dot(weight_series)
    cumulative_returns = (1 + portfolio_daily_returns).cumprod() - 1
    
    return portfolio_daily_returns, cumulative_returns

def calculate_volatility(daily_returns: pd.Series, trading_days: int = 252) -> float:
    """Calculates annualized volatility standard deviation."""
    if daily_returns.empty:
        return 0.0
    return float(daily_returns.std() * np.sqrt(trading_days))

def calculate_max_drawdown(cumulative_returns: pd.Series) -> float:
    """Calculates Maximum Drawdown (MDD) peak-to-trough drop."""
    if cumulative_returns.empty:
        return 0.0
    portfolio_val = 1.0 + cumulative_returns
    peak = portfolio_val.cummax()
    drawdown = (portfolio_val - peak) / peak
    return float(abs(drawdown.min()))

def calculate_sharpe_ratio(
    daily_returns: pd.Series, 
    annualized_volatility: float, 
    risk_free_rate: float = 0.02
) -> float:
    """Calculates Risk-Adjusted Return (Sharpe Ratio)."""
    if annualized_volatility == 0 or daily_returns.empty:
        return 0.0
    total_days = len(daily_returns)
    if total_days == 0:
        return 0.0
    
    total_return = (1 + daily_returns).prod() - 1
    annualized_return = (1 + total_return) ** (252 / total_days) - 1
    
    return float((annualized_return - risk_free_rate) / annualized_volatility)

def calculate_risk_contributions(
    price_df: pd.DataFrame, 
    weights: Dict[str, float]
) -> Dict[str, float]:
    """Calculates factor risk contribution: which asset contributes most to portfolio risk."""
    returns = price_df.pct_change().dropna()
    tickers = list(weights.keys())
    
    valid_tickers = [t for t in tickers if t in returns.columns]
    if not valid_tickers:
        return {t: 1.0 / len(tickers) for t in tickers}
    
    w = np.array([weights[t] for t in valid_tickers])
    w = w / np.sum(w)
    
    cov_matrix = returns[valid_tickers].cov().to_numpy()
    portfolio_var = np.dot(w.T, np.dot(cov_matrix, w))
    
    if portfolio_var == 0:
        return {t: 1.0 / len(valid_tickers) for t in valid_tickers}
    
    marginal_contrib = np.dot(cov_matrix, w)
    risk_contrib = (w * marginal_contrib) / portfolio_var
    
    abs_risk_contrib = np.abs(risk_contrib)
    normalized_risk_contrib = abs_risk_contrib / np.sum(abs_risk_contrib)
    
    return {ticker: float(round(contrib, 4)) for ticker, contrib in zip(valid_tickers, normalized_risk_contrib)}
