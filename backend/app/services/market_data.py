import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import CachedMarketData

def get_current_price(ticker_symbol: str) -> float:
    """Fetches real-time closing or current price for a ticker symbol."""
    clean_ticker = ticker_symbol.upper().strip()
    try:
        ticker = yf.Ticker(clean_ticker)
        
        # Try fast_info first
        fast_info = getattr(ticker, "fast_info", None)
        if fast_info and "lastPrice" in fast_info and fast_info["lastPrice"] is not None:
            return float(fast_info["lastPrice"])
            
        # Fallback to history 1d
        hist = ticker.history(period="1d")
        if hist.empty:
            raise HTTPException(status_code=404, detail=f"Ticker symbol '{clean_ticker}' not found.")
            
        if isinstance(hist.columns, pd.MultiIndex):
            hist.columns = hist.columns.get_level_values(0)
            
        close_val = hist["Close"].iloc[-1]
        if isinstance(close_val, pd.Series):
            close_val = close_val.iloc[0]
            
        return float(close_val)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail=f"Failed to fetch market price for '{clean_ticker}': {str(e)}")

def get_batch_historical_prices(tickers: List[str], period: str = "1y") -> pd.DataFrame:
    """
    Vectorized batch downloader for multiple assets using yfinance.
    Cleans MultiIndex headers, aligns dates across exchanges, and fills gaps.
    """
    clean_tickers = list(dict.fromkeys([t.upper().strip() for t in tickers if t and t.strip()]))
    if not clean_tickers:
        return pd.DataFrame()
        
    try:
        # Download all assets in a single batch request
        data = yf.download(clean_tickers, period=period, progress=False, auto_adjust=True)
        
        if data.empty:
            return pd.DataFrame()
            
        # Extract Close prices
        if isinstance(data.columns, pd.MultiIndex):
            if "Close" in data.columns.levels[0]:
                close_df = data["Close"]
            else:
                close_df = data.iloc[:, :len(clean_tickers)]
        elif "Close" in data:
            close_df = data[["Close"]]
        else:
            close_df = data

        if isinstance(close_df, pd.Series):
            close_df = pd.DataFrame({clean_tickers[0]: close_df})
            
        # Clean column names
        close_df.columns = [str(col).upper() for col in close_df.columns]
        
        # Filter for requested clean tickers
        available_cols = [t for t in clean_tickers if t in close_df.columns]
        if not available_cols:
            return pd.DataFrame()
            
        price_matrix = close_df[available_cols].copy()
        
        # Forward fill and backward fill for holidays/date alignment across assets
        price_matrix = price_matrix.ffill().bfill().dropna()
        
        return price_matrix
    except Exception as e:
        print(f"yfinance Batch Download Error: {e}")
        return pd.DataFrame()

def fetch_historical_data(ticker_symbol: str, period: str = "1y") -> pd.DataFrame:
    """Single ticker historical fetch wrapper returning structured records."""
    df = get_batch_historical_prices([ticker_symbol], period=period)
    if df.empty or ticker_symbol.upper() not in df.columns:
        return pd.DataFrame()
        
    clean_ticker = ticker_symbol.upper()
    records = []
    for date, price in df[clean_ticker].items():
        records.append({
            "ticker": clean_ticker,
            "date": date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date),
            "close_price": float(price),
            "volume": 0
        })
    return pd.DataFrame(records)

def cache_historical_data(db: Session, ticker: str, records: List[Dict[str, Any]]):
    """Persists historical records into database non-blockingly."""
    try:
        if not records:
            return
        clean_ticker = ticker.upper()
        existing_dates = set(
            row[0] for row in db.query(CachedMarketData.date)
            .filter(CachedMarketData.ticker == clean_ticker).all()
        )
        new_objects = []
        for r in records:
            date_str = str(r["date"])
            if date_str not in existing_dates:
                new_objects.append(
                    CachedMarketData(
                        ticker=clean_ticker,
                        date=date_str,
                        close_price=float(r["close_price"]),
                        volume=int(r.get("volume", 0))
                    )
                )
        if new_objects:
            db.bulk_save_objects(new_objects)
            db.commit()
    except Exception:
        db.rollback()
