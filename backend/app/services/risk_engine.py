from typing import Dict, Any

def classify_portfolio_risk(
    volatility: float, 
    max_drawdown: float, 
    asset_count: int
) -> Dict[str, Any]:
    """Classifies portfolio risk score (0-100) and risk level (Low/Medium/High)."""
    vol_score = min(volatility / 0.35, 1.0) * 50
    mdd_score = min(max_drawdown / 0.40, 1.0) * 40
    
    concentration_penalty = 10.0 if asset_count <= 1 else max(0.0, 10.0 - (asset_count * 2.0))
    
    risk_score = round(vol_score + mdd_score + concentration_penalty, 2)
    risk_score = min(max(risk_score, 0.0), 100.0)
    
    if risk_score < 35.0:
        risk_level = "Low"
        explanation = "Portfolio exhibits low volatility and minimal historical drawdowns with balanced diversification."
    elif risk_score < 70.0:
        risk_level = "Medium"
        explanation = "Portfolio shows moderate price fluctuations. Standard risk-return trade-off profile."
    else:
        risk_level = "High"
        explanation = "Portfolio is subject to substantial volatility, significant drawdown risk, or single-asset concentration."

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "explanation": explanation,
        "metrics_summary": {
            "volatility": round(volatility, 4),
            "max_drawdown": round(max_drawdown, 4),
            "asset_count": asset_count
        }
    }
