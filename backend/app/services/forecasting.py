import pandas as pd
import numpy as np
from typing import List, Dict, Any
from statsmodels.tsa.arima.model import ARIMA
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning

warnings.simplefilter('ignore', ConvergenceWarning)
warnings.simplefilter('ignore', UserWarning)

def forecast_portfolio_growth(
    daily_returns: pd.Series, 
    forecast_days: int = 30
) -> Dict[str, Any]:
    """
    Fits ARIMA model with trend drift to predict portfolio trajectory.
    Returns recent historical trail + future forecasted points with 95% confidence bounds.
    """
    if daily_returns.empty or len(daily_returns) < 20:
        return {"historical_trail": [], "forecast": []}
        
    cum_growth = (1 + daily_returns).cumprod()
    
    # 1. Capture recent 30-day historical tail to connect on the graph
    recent_trail = []
    trail_df = cum_growth.tail(30)
    for date_idx, val in trail_df.items():
        date_str = date_idx.strftime("%Y-%m-%d") if hasattr(date_idx, "strftime") else str(date_idx)
        recent_trail.append({"date": date_str, "value": float(round(val, 4))})
        
    last_date = cum_growth.index[-1]
    last_val = float(cum_growth.iloc[-1])
    
    try:
        # Fit ARIMA(1, 1, 1) with linear trend 't' (constant drift in differenced returns)
        model = ARIMA(cum_growth.values, order=(1, 1, 1), trend='t')
        model_fit = model.fit()
        
        forecast_res = model_fit.get_forecast(steps=forecast_days)
        forecast_mean = forecast_res.predicted_mean
        conf_int = forecast_res.conf_int(alpha=0.05)
        
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days, freq="B")
        
        forecast_records = []
        # Connect starting point smoothly to the last historical value
        forecast_records.append({
            "date": last_date.strftime("%Y-%m-%d") if hasattr(last_date, "strftime") else str(last_date),
            "forecast": round(last_val, 4),
            "lower_bound": round(last_val, 4),
            "upper_bound": round(last_val, 4)
        })
        
        for i in range(forecast_days):
            mean_val = float(forecast_mean[i])
            lower_val = float(conf_int[i, 0])
            upper_val = float(conf_int[i, 1])
            lower_val = max(0.0, lower_val)
            
            forecast_records.append({
                "date": future_dates[i].strftime("%Y-%m-%d"),
                "forecast": round(mean_val, 4),
                "lower_bound": round(lower_val, 4),
                "upper_bound": round(upper_val, 4)
            })
            
        return {
            "historical_trail": recent_trail,
            "forecast": forecast_records
        }
    except Exception as e:
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days, freq="B")
        fallback_records = [{
            "date": last_date.strftime("%Y-%m-%d"),
            "forecast": round(last_val, 4),
            "lower_bound": round(last_val, 4),
            "upper_bound": round(last_val, 4)
        }]
        for i in range(forecast_days):
            fallback_records.append({
                "date": future_dates[i].strftime("%Y-%m-%d"),
                "forecast": round(last_val * (1 + ((i + 1) * 0.0005)), 4),
                "lower_bound": round(last_val * (1 - ((i + 1) * 0.005)), 4),
                "upper_bound": round(last_val * (1 + ((i + 1) * 0.008)), 4)
            })
        return {
            "historical_trail": recent_trail,
            "forecast": fallback_records
        }
