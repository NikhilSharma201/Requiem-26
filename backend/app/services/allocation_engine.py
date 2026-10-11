from typing import Dict

def generate_recommended_allocation(
    current_weights: Dict[str, float], 
    target_risk: str
) -> Dict[str, float]:
    """Adjusts asset weights according to the specified risk target."""
    tickers = list(current_weights.keys())
    n_assets = len(tickers)
    
    if n_assets == 0:
        return {}
    if n_assets == 1:
        return {tickers[0]: 1.0}
        
    equal_weight = 1.0 / n_assets
    recommended = {}
    
    target_risk_upper = target_risk.capitalize()
    
    if target_risk_upper == "Low":
        for ticker, weight in current_weights.items():
            recommended[ticker] = (weight * 0.3) + (equal_weight * 0.7)
    elif target_risk_upper == "Medium":
        for ticker, weight in current_weights.items():
            recommended[ticker] = (weight * 0.6) + (equal_weight * 0.4)
    else:  # High Risk
        total = sum(current_weights.values())
        for ticker, weight in current_weights.items():
            recommended[ticker] = weight / total
            
    rec_sum = sum(recommended.values())
    normalized_rec = {t: round(w / rec_sum, 4) for t, w in recommended.items()}
    
    diff = round(1.0 - sum(normalized_rec.values()), 4)
    first_key = list(normalized_rec.keys())[0]
    normalized_rec[first_key] = round(normalized_rec[first_key] + diff, 4)

    return normalized_rec
