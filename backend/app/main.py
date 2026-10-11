from fastapi import FastAPI
from app.database import engine, Base
from app.routers import portfolios, market, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Investment Risk Prediction API",
    description="ML-based portfolio analysis and risk prediction platform.",
    version="1.0.0"
)

app.include_router(portfolios.router)
app.include_router(market.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Investment Risk Prediction API is online"}
