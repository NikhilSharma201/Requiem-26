from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.post("/", response_model=schemas.PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(payload: schemas.PortfolioCreate, db: Session = Depends(get_db)):
    total_allocation = sum(asset.allocation_percentage for asset in payload.assets)
    if round(total_allocation, 2) != 100.00:
        raise HTTPException(
            status_code=400,
            detail=f"Allocation percentages must sum to 100, got {total_allocation}"
        )

    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user:
        user = models.User(username=payload.username, risk_preference=payload.risk_preference)
        db.add(user)
        db.commit()
        db.refresh(user)

    portfolio = models.Portfolio(user_id=user.id, total_investment=payload.total_investment)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    for asset in payload.assets:
        db.add(models.PortfolioAsset(
            portfolio_id=portfolio.id,
            ticker_symbol=asset.ticker_symbol.upper(),
            allocation_percentage=asset.allocation_percentage
        ))
    db.commit()
    db.refresh(portfolio)

    return portfolio


@router.get("/{portfolio_id}", response_model=schemas.PortfolioResponse)
def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio
