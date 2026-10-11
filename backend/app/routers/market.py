from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.services import market_data

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/price/{ticker}", response_model=schemas.PriceResponse)
def get_price(ticker: str):
    try:
        price = market_data.get_current_price(ticker.upper())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"ticker": ticker.upper(), "price": price}


@router.get("/history/{ticker}", response_model=schemas.HistoricalDataResponse)
def get_history(ticker: str, period: str = Query("1y"), db: Session = Depends(get_db)):
    try:
        records = market_data.fetch_historical_data(ticker.upper(), period=period)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    market_data.cache_historical_data(db, ticker.upper(), records)
    return {"ticker": ticker.upper(), "data": records}
