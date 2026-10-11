from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class AssetInput(BaseModel):
    ticker_symbol: str
    allocation_percentage: float = Field(..., gt=0, le=100)


class PortfolioCreate(BaseModel):
    username: str
    risk_preference: str = "Medium"
    total_investment: float = Field(..., gt=0)
    assets: List[AssetInput]


class AssetResponse(BaseModel):
    ticker_symbol: str
    allocation_percentage: float

    class Config:
        from_attributes = True


class PortfolioResponse(BaseModel):
    id: int
    user_id: int
    total_investment: float
    created_at: datetime
    assets: List[AssetResponse]

    class Config:
        from_attributes = True


class PriceResponse(BaseModel):
    ticker: str
    price: float


class HistoricalPricePoint(BaseModel):
    date: str
    close_price: float
    volume: Optional[int] = None


class HistoricalDataResponse(BaseModel):
    ticker: str
    data: List[HistoricalPricePoint]
