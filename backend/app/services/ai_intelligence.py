from typing import Dict, List, Any

def generate_ai_market_intelligence(
    allocations: Dict[str, float],
    risk_level: str,
    volatility: float,
    max_drawdown: float,
    top_risk_asset: str
) -> Dict[str, Any]:
    """
    Generates qualitative AI market intelligence insights based on portfolio parameters,
    sector exposure heuristics, and volatility indicators.
    """
    tickers = list(allocations.keys())
    
    # Analyze asset characteristics
    bonds_and_safeties = {"BND", "AGG", "TLT", "IEF", "SHY", "GLD", "IAU"}
    tech_growth = {"AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"}
    
    fixed_income_alloc = sum(allocations.get(t, 0.0) for t in bonds_and_safeties)
    tech_alloc = sum(allocations.get(t, 0.0) for t in tech_growth)
    
    bullet_points = []
    
    # 1. Macroeconomic Context
    if fixed_income_alloc > 0.3:
        bullet_points.append("🛡️ **Fixed-Income Cushion:** Significant allocation to defensive/bond assets provides downside protection during equity market contractions.")
    elif tech_alloc > 0.5:
        bullet_points.append("🚀 **High Growth Concentration:** Over 50% of the portfolio is allocated to high-beta technology/growth stocks, making performance sensitive to interest rate policy shifts.")
    else:
        bullet_points.append("⚖️ **Balanced Equity Mix:** Portfolio reflects a multi-sector allocation pattern across equities.")

    # 2. Key Risk Driver Insight
    bullet_points.append(f"⚠️ **Primary Volatility Driver:** Market covariance analysis indicates **{top_risk_asset}** contributes most significantly to total portfolio risk variance.")

    # 3. Macro Outlook & Recommendation
    if volatility > 0.25:
        bullet_points.append("📉 **Macro Regime Warning:** Annualized volatility exceeds 25%. Consider rebalancing into low-beta assets or Treasury bonds to mitigate potential drawdown spikes.")
    else:
        bullet_points.append("✅ **Stability Check:** Volatility remains within standard institutional bounds (<25%). Strategy is resilient against minor market fluctuations.")

    headline = f"AI Analysis: {risk_level} Risk Profile with {tech_alloc*100:.0f}% Tech & {fixed_income_alloc*100:.0f}% Defensive Allocation"

    return {
        "headline": headline,
        "insights": bullet_points,
        "tech_exposure_pct": round(tech_alloc * 100, 2),
        "defensive_exposure_pct": round(fixed_income_alloc * 100, 2)
    }
