# 📈 Investment Risk Prediction & Portfolio Optimization System

> **A Test-Driven, ML-Powered Portfolio Risk Evaluation & Allocation Platform**  
> Built with FastAPI, Streamlit, PostgreSQL, `yfinance`, `scikit-learn`, and `statsmodels` (ARIMA).

---

## 📌 Executive Summary

The **Investment Risk Prediction System** is a financial intelligence platform that evaluates portfolio risk, predicts future value trajectories, identifies single-asset risk drivers, and recommends dynamic re-allocation strategies based on user risk preferences. 

By integrating **Modern Portfolio Theory (MPT)** with **Machine Learning feature scoring** and **ARIMA time-series forecasting**, the system translates complex financial metrics into actionable, plain-English insights and interactive visual dashboards.

---

## 🏗️ System Architecture & Technology Stack

The platform utilizes a **decoupled 3-tier architecture** designed for high throughput, low-latency vectorized calculations, and non-blocking database writes.
┌─────────────────────────────────────────────────────────────────────────────┐
│ FRONTEND (STREAMLIT) │
│ - Interactive Sidebar Controls (Tickers, Weights, Risk Level, Horizon) │
│ - Plotly Visualizations (Risk Pie, Allocation Bar, Growth, ARIMA, Map) │
└──────────────────────────────────────┬──────────────────────────────────────┘
│ HTTP POST /analytics/evaluate
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ BACKEND (FASTAPI) │
│ - REST Routers (Analytics, Market Ingestion, Portfolios) │
│ - Schema Validation via Pydantic V2 │
│ - Async Uvicorn ASGI Server │
└──────────────┬───────────────────────┬───────────────────────┬──────────────┘
│ │ │
▼ ▼ ▼
┌──────────────────────────┐ ┌───────────────────┐ ┌──────────────────────────┐
│ yFINANCE MARKET DATA │ │ ENGINE SUITE │ │ DATABASE (PostgreSQL) │
│ Vectorized Batch Fetch │ │ - Risk Scorer │ │ SQLAlchemy ORM │
│ Holiday/Date Auto-Fill │ │ - Allocator │ │ Cached Historical Data │
│ MultiIndex Parser │ │ - ARIMA Engine │ │ User & Portfolio Models │
└──────────────────────────┘ └───────────────────┘ └──────────────────────────┘

text


### 🛠️ Tech Stack Specifications

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Frontend UI** | `Streamlit` | Reactive dashboard managing dynamic session state and auto-updating visualizations. |
| **Data Visualization** | `Plotly Express` / `Graph Objects` | Render engine for Factor Risk, Re-allocation Comparison, Growth, and ARIMA CI Bands. |
| **Backend REST API** | `FastAPI` + `Uvicorn` | Asynchronous backend API engine executing financial pipelines and schema validation. |
| **Market Data** | `yfinance` | Vectorized batch fetching of 1-year historical daily prices aligned across global markets. |
| **Data Processing** | `pandas` + `numpy` | Linear algebra, covariance matrix computation, and daily return calculations. |
| **Machine Learning** | `scikit-learn` / Feature Scorer | Dynamic risk scoring (0–100) and risk tier categorization. |
| **Time-Series Forecast** | `statsmodels` (ARIMA) | ARIMA(1,1,1) model with trend drift for 7 to 90-day future portfolio path projections. |
| **Database & ORM** | `PostgreSQL` + `SQLAlchemy` | Relational persistence for Users, Portfolios, Allocations, and Market Data Cache. |
| **Test Suite** | `pytest` + `httpx` | 100% test-driven development (TDD) coverage across math services and API endpoints. |

---

## 🎯 Key Features Breakdown

### 1. Live Market Data Ingestion
* Vectorized batch downloading via `yfinance` to eliminate row-by-row request latency.
* MultiIndex column flattening and automatic date alignment across different exchange calendars.

### 2. Quantitative & ML Risk Engine
* **Risk Meter (0–100 Score):** Scores portfolio risk using a weighted formula combining volatility, maximum drawdown, and asset concentration.
* **Risk Categorization:** Classifies portfolios into `Low Risk`, `Medium Risk`, or `High Risk` tiers.
* **Factor Risk Contribution:** Uses covariance matrix analysis to isolate which stock drives the highest variance.

### 3. Strategy Re-Allocation Engine
* Generates target portfolio weights smoothed toward equal-weighted diversification to match desired risk profiles (`Low`, `Medium`, `High`).

### 4. Multi-Strategy Historical Backtesting
* 1-year time-machine growth simulation comparing:
  1. **User Original Portfolio**
  2. **ML Recommended Allocation**
  3. **Equal-Weighted Strategy**
  4. **Market Benchmark** (S&P 500 `^GSPC`, NASDAQ-100 `^NDX`, NIFTY 50 `^NSEI`, or VT)

### 5. ARIMA Time-Series Forecasting
* Projects future portfolio value over **7, 14, 30, 60, or 90 trading days**.
* Generates a **95% Confidence Interval band** (fan chart/funnel) modeling compounding market uncertainty.
* Connects seamlessly to the recent 30-day historical actuals line.

### 6. Macro Stress-Testing & Asset Map
* **Stress Test Engine:** Simulates capital impact during macroeconomic shocks (e.g., 2008 Financial Crisis -30%, Tech Crash -20%).
* **Risk vs. Return Map:** Plotly scatter map positioning assets on Volatility ($\sigma$) vs Return ($R$) axes.

### 7. AI Qualitative Market Intelligence
* Generates plain-English narrative reports detailing tech concentration, defensive bond padding, and macro interest rate vulnerabilities.

---

## 🧠 Mathematical Models & Risk Prediction Basis

### 🔍 On What Basis Do We Predict Risk?

Our system evaluates portfolio risk across **3 Quantitative Pillars**:

$$\mathbf{\text{Total Risk Score}} = \mathbf{\text{Vol\_Score} + \text{MDD\_Score} + \text{Penalty}}$$
text

                 ┌─────────────────────────────────────────┐
                 │            TOTAL RISK SCORE             │
                 │                (0 - 100)                │
                 └────────────────────┬────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│ ANNUAL VOLATILITY (σ) │ │ MAX DRAWDOWN (MDD) │ │ CONCENTRATION PENALTY │
│ Weight: 50% │ │ Weight: 40% │ │ Weight: 10% │
│ Measures instability │ │ Measures peak-to- │ │ Penalizes single-asset│
│ of daily price │ │ trough worst drop │ │ dependency/lack of │
│ fluctuations │ │ over past 1 year │ │ diversification │
└───────────────────────┘ └───────────────────────┘ └───────────────────────┘

text


#### 1. Annualized Volatility ($\sigma_{annual}$) — *Weight: 50%*
Calculates standard deviation of portfolio daily returns scaled across 252 annual trading days:

$$r_t = \frac{P_t - P_{t-1}}{P_{t-1}}, \quad R_{p,t} = \sum (r_{i,t} \cdot w_i)$$

$$\sigma_{annual} = \text{StdDev}(R_{p,t}) \times \sqrt{252}$$

$$\text{Vol\_Score} = \min\left(\frac{\sigma_{annual}}{0.35}, 1.0\right) \times 50$$

#### 2. Maximum Drawdown ($MDD$) — *Weight: 40%*
Evaluates worst peak-to-trough capital decline over 1 year to measure downside loss risk:

$$V_t = \prod_{k=1}^{t} (1 + R_{p,k}), \quad \text{Peak}_t = \max_{1 \le k \le t} (V_k)$$

$$MDD = \max_{t} \left( \frac{\text{Peak}_t - V_t}{\text{Peak}_t} \right)$$

$$\text{MDD\_Score} = \min\left(\frac{MDD}{0.40}, 1.0\right) \times 40$$

#### 3. Concentration Penalty ($C$) — *Weight: 10%*
Penalizes portfolios for lack of asset diversification:

$$\text{Penalty} = \max(0.0, 10.0 - (\text{Asset Count} \times 2.0))$$

---

### 🚦 Classification Thresholds

| Total Score | Risk Tier | Description |
| :--- | :--- | :--- |
| **0.0 – 34.9** | 🟢 **Low Risk** | Low volatility ($<12\%$), minimal drawdowns ($<8\%$), heavy defensive asset weight. |
| **35.0 – 69.9** | 🟡 **Medium Risk** | Standard equity volatility ($12\% - 25\%$), balanced risk-return profile. |
| **70.0 – 100.0**| 🔴 **High Risk** | High volatility ($>25\%$), severe drawdown potential ($>25\%$), or single-asset concentration. |

---

### 🎯 Covariance Risk Contribution (Factor Breakdown)

Isolates which asset contributes the most to overall portfolio variance using the Covariance Matrix ($\Sigma$):

$$\text{Portfolio Variance } \sigma_p^2 = w^T \Sigma w$$

$$\text{Risk Contribution}_i = \frac{w_i \cdot (\Sigma w)_i}{\sigma_p^2}$$

---

### 🔮 ARIMA(1,1,1) Time-Series Forecasting Model

Predicts future portfolio growth paths over a user-selected horizon ($H \in \{7, 14, 30, 60, 90\}$ days) using an AutoRegressive Integrated Moving Average model with trend drift:

$$y_t' = c + \phi_1 y_{t-1}' + \theta_1 \epsilon_{t-1} + \epsilon_t$$

Where $y_t'$ is the first-differenced cumulative return series ($y_t - y_{t-1}$).

#### 📈 Understanding the 95% Confidence Interval Band (Funnel)
* **Center Line:** Expected mean forecast baseline ($y_{forecast}$).
* **Shaded Fan Band:** 95% Confidence bounds modeling compounding market volatility over time:

$$\text{Confidence Interval} = \hat{y}_t \pm 1.96 \times \text{SE}(\hat{y}_t)$$

* As the forecast horizon extends into the future, uncertainty increases, causing the confidence band to widen naturally.

---

## 🗄️ Database Schema (PostgreSQL)
┌───────────────────────────┐ ┌───────────────────────────────────────┐
│ USERS │ │ PORTFOLIOS │
├───────────────────────────┤ ├───────────────────────────────────────┤
│ id (PK, String) │1 * │ id (PK, Integer) │
│ username (String) ├─────────┤ user_id (FK -> users.id) │
│ risk_pref (String) │ │ total_investment (Float) │
│ created_at (DateTime) │ │ created_at (DateTime) │
└───────────────────────────┘ └──────────────────┬────────────────────┘
│ 1
│
│ *
┌──────────────────┴────────────────────┐
│ PORTFOLIO_ASSETS │
├───────────────────────────────────────┤
│ id (PK, Integer) │
│ portfolio_id (FK -> portfolios) │
│ ticker_symbol (String) │
│ allocation_pct (Float) │
└───────────────────────────────────────┘

text


---

## ⚡ Setup & Installation Guide

### Prerequisites
* **OS:** Linux / Ubuntu (or macOS / WSL)
* **Python:** Python 3.11
* **Database:** PostgreSQL (local or remote instance)

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/your-username/investment-risk-prediction.git
cd investment-risk-prediction

# Create Python 3.11 venv
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
2. Configure Environment Variables
Create a .env file in the project root:

env

DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/investment_risk_db
TEST_DATABASE_URL=sqlite:///:memory:
3. Run Pytest Test Suite (TDD Verification)
Ensure all 21 unit and API integration tests pass:

Bash

PYTHONPATH=backend pytest -v
🚀 Running the Application
Launch the backend and frontend in separate terminal windows:

Terminal 1: Launch FastAPI Backend
Bash

cd ~/investment-risk-prediction
source venv/bin/activate

uvicorn app.main:app --app-dir backend --reload --port 8000
Swagger UI API Docs: http://127.0.0.1:8000/docs
Terminal 2: Launch Streamlit Dashboard
Bash

cd ~/investment-risk-prediction
source venv/bin/activate

streamlit run frontend/app.py
Web Interface: http://localhost:8501
📡 API Endpoint Reference
POST /analytics/evaluate
Evaluates portfolio risk metrics, ARIMA predictions, and allocation recommendations.

Request Body
JSON

{
  "allocations": {
    "AAPL": 0.30,
    "MSFT": 0.25,
    "TSLA": 0.20,
    "BND": 0.15,
    "GOOGL": 0.10
  },
  "target_risk": "Low",
  "benchmark": "^GSPC",
  "forecast_days": 30
}
Response Payload (Excerpt)
JSON

{
  "risk_level": "Medium",
  "risk_score": 40.5,
  "explanation": "Portfolio exhibits moderate price fluctuations...",
  "annualized_volatility": 0.1731,
  "max_drawdown": 0.1575,
  "sharpe_ratio": 0.76,
  "risk_contributions": {
    "TSLA": 0.417,
    "AAPL": 0.221,
    "MSFT": 0.198,
    "GOOGL": 0.137,
    "BND": 0.027
  },
  "recommended_allocation": {
    "AAPL": 0.23,
    "MSFT": 0.21,
    "TSLA": 0.18,
    "BND": 0.23,
    "GOOGL": 0.15
  },
  "ai_market_intelligence": {
    "headline": "AI Analysis: Medium Risk Profile with 85% Tech...",
    "insights": [
      "🚀 High Growth Concentration...",
      "⚠️ Primary Volatility Driver: TSLA..."
    ]
  },
  "historical_growth": [...],
  "arima_forecast": {
    "historical_trail": [...],
    "forecast": [...]
  }
}
📄 License
This project is open-source and available under the MIT License.
