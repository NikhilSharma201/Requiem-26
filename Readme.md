# 📈 Investment Risk Prediction & Portfolio Optimization System

> A test-driven, ML-powered portfolio risk evaluation, allocation, and ARIMA forecasting platform.
>
> Built with FastAPI, Streamlit, PostgreSQL, `yfinance`, `scikit-learn`, and `statsmodels`.

## Overview

The Investment Risk Prediction System helps investors either:

- build an optimized portfolio from scratch, or
- improve an existing portfolio by detecting hidden concentration and volatility risks.

It combines:

- Modern Portfolio Theory (MPT)
- ML-based risk scoring
- ARIMA forecasting
- portfolio stress testing
- portfolio optimization

The platform evaluates historical market behavior, identifies risky asset concentration, and recommends better allocations aligned with the user's target risk profile.

---

## Dual Workflow Modes

When users launch the platform, they can choose between two operational workflows:

```text
┌──────────────────────────────────────────────┐
│        SELECT WORKFLOW OPERATING MODE       │
└───────────────────────┬──────────────────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
┌──────────────────────────────┐  ┌────────────────────────────────┐
│   MODE 1: BUILD FROM SCRATCH │  │ MODE 2: ENHANCE EXISTING      │
│                              │  │                                │
│ • Capital input               │  │ • Custom ticker portfolio      │
│ • Risk target selection      │  │ • Weight allocation input     │
│ • Theme selection             │  │ • Hidden risk driver scan     │
│ • Auto-optimized basket      │  │ • Risk-based redistribution   │
└──────────────────────────────┘  └────────────────────────────────┘
```

### Mode 1: Build from Scratch

Users provide:

- total investment capital
- target risk level (Low / Medium / High)
- investment theme

The system constructs a portfolio with an optimized asset basket and projected performance metrics.

### Mode 2: Enhance Existing Portfolio

Users provide:

- their current stock allocation
- stock weights
- optional custom tickers

The system identifies concentration risk, ill-diversified holdings, and recommends reallocation weights to improve risk-adjusted outcomes.

---

## System Architecture

```mermaid
flowchart LR
    UI[Streamlit Frontend] -->|HTTP API Calls| API[FastAPI Backend]
    API -->|Fetch market data| YF[yfinance]
    API -->|Risk analysis| RS[Risk Scoring Engine]
    API -->|Allocation optimization| OPT[Portfolio Optimizer]
    API -->|Forecasting| ARIMA[ARIMA Model]
    API -->|Store models and results| DB[(PostgreSQL)]
    UI -->|Visualization| PLOT[Plotly Dashboards]
```

### Architecture Summary

- Frontend: Streamlit dashboard for workflow selection, interactive controls, and visual analytics
- Backend: FastAPI REST API with route-driven evaluation logic
- Market Data: yfinance for historical data ingestion
- Risk Engine: Quantitative scoring using volatility, max drawdown, and concentration metrics
- Forecasting: ARIMA-based future portfolio projection
- Persistence: SQLAlchemy + PostgreSQL for portfolios and user data

---

## Key Features

### 1. Dual Portfolio Modes

- Build from scratch using target risk and capital inputs
- Enhance an existing allocation with optimization suggestions

### 2. Historical Lookback Analysis

Analyze performance over:

- 3 months
- 6 months
- 1 year
- 2 years

### 3. Profit and Loss Metrics

The platform calculates:

- net profit / loss
- ROI percentage
- scenario comparisons

### 4. Quantitative Risk Engine

A composite risk score is formed using:

- annualized volatility
- maximum drawdown
- concentration penalty

### 5. Reallocation Engine

It recommends improved portfolio weights to:

- reduce volatility
- increase diversification
- align with target risk preferences

### 6. Historical Backtesting

It compares multiple strategies, including:

1. original portfolio
2. ML recommended portfolio
3. equal-weighted portfolio
4. benchmark portfolio

### 7. ARIMA Forecasting

It projects future portfolio values over:

- 7 days
- 14 days
- 30 days
- 60 days
- 90 days

It also generates a 95% confidence interval band.

### 8. Risk-Return Mapping

It plots assets on a volatility vs return map to visualize trade-offs.

---

## Mathematical Basis of Risk Prediction

The system evaluates portfolio risk across three pillars:

```text
Total Risk Score = Volatility Score + MDD Score + Concentration Penalty
```

### 1. Annualized Volatility

```text
r_t = (P_t - P_(t-1)) / P_(t-1)
R_p,t = Σ(r_i,t × w_i)
σ_annual = StdDev(R_p,t) × √252
```

### 2. Maximum Drawdown

```text
V_t = Π(1 + R_p,k)
Peak_t = max(V_k)
MDD = max((Peak_t - V_t) / Peak_t)
```

### 3. Concentration Penalty

```text
Penalty = max(0, 10 - (Asset Count × 2))
```

### ARIMA Forecast Model

```text
y_t' = c + φ_1 y_(t-1)' + θ_1 ε_(t-1) + ε_t
```

This is used to forecast future portfolio growth over the selected horizon and estimate uncertainty via confidence intervals.

---

## Database Schema

```mermaid
erDiagram
    USERS ||--o{ PORTFOLIOS : owns
    PORTFOLIOS ||--o{ PORTFOLIO_ASSETS : contains

    USERS {
        string id PK
        string username
        string risk_pref
        datetime created_at
    }

    PORTFOLIOS {
        int id PK
        string user_id FK
        float total_investment
        datetime created_at
    }

    PORTFOLIO_ASSETS {
        int id PK
        int portfolio_id FK
        string ticker_symbol
        float allocation_pct
    }
```

---

## Demo Test Data Sets

These tickers can be used to demo Mode 2 behavior:

| Scenario | Tickers & Allocation | Expected Result |
| --- | --- | --- |
| High Volatility & Crypto | `MSTR` (35%), `COIN` (25%), `PLTR` (20%), `META` (20%) | High risk |
| Defensive Preservation | `KO` (30%), `JNJ` (30%), `WM` (20%), `TLT` (20%) | Low risk |
| Blue-Chip Financials | `JPM` (30%), `XOM` (25%), `PG` (25%), `CAT` (20%) | Medium risk |
| Global & Commodities | `TSM` (30%), `NVO` (25%), `SLV` (25%), `ASML` (20%) | Medium risk |

---

## Project Structure

```text
Requiem-26/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routers/
│   ├── tests/
│   ├── pytest.ini
│   └── test.db
├── frontend/
│   └── app.py
├── .env
├── requirements.txt
├── Readme.md
├── test.db
└── venv/
```

---

## Setup & Execution Guide

### Prerequisites

- Python 3.11+
- PostgreSQL (local or remote instance)
- Virtual environment enabled

### 1. Clone the repository

```bash
git clone https://github.com/NikhilSharma201/Requiem-26.git
cd Requiem-26
```

### 2. Create and activate the virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/investment_risk_db
TEST_DATABASE_URL=sqlite:///:memory:
```

### 5. Run the test suite

```bash
PYTHONPATH=backend pytest -v
```

### 6. Run the backend server

```bash
cd ~/Requiem-26
source venv/bin/activate
uvicorn app.main:app --app-dir backend --reload --port 8000
```

API docs: `http://127.0.0.1:8000/docs`

### 7. Run the Streamlit dashboard

```bash
cd ~/Requiem-26
source venv/bin/activate
streamlit run frontend/app.py
```

Dashboard URL: `http://localhost:8501`

---

## Technology Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Frontend UI | `Streamlit` | Interactive dashboard and workflow selection |
| Data Visualization | `Plotly` | Charts, forecasts, and portfolio maps |
| Backend API | `FastAPI` + `Uvicorn` | Risk evaluation and portfolio APIs |
| Market Data | `yfinance` | Historical market and ticker data |
| Data Processing | `pandas` + `numpy` | Returns, covariance, and optimization calculations |
| Machine Learning | `scikit-learn` | Risk feature scoring and portfolio classification |
| Time-Series Forecasting | `statsmodels` (ARIMA) | Forecasting future portfolio values |
| Database | `PostgreSQL` + `SQLAlchemy` | Storage for users, portfolios, and allocations |
| Test Suite | `pytest` + `httpx` | Automated verification and API checks |

---

## License

This project is open-source and available under the MIT License.

---

## Summary

This project combines portfolio optimization, machine learning risk analysis, and time-series forecasting into a single decision-support platform for investment analysis and strategic rebalancing.
