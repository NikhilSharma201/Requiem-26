# 📈 Investment Risk Prediction & Portfolio Optimization System

> **A Test-Driven, ML-Powered Portfolio Risk Evaluation, Allocation & ARIMA Forecasting Platform**  
> Built with FastAPI, Streamlit, PostgreSQL, `yfinance`, `scikit-learn`, and `statsmodels` (ARIMA).

---

## 📌 Executive Summary

The **Investment Risk Prediction System** is an end-to-end financial intelligence platform that empowers investors to either **build an optimal portfolio from scratch** or **enhance an existing stock portfolio**. 

By combining **Modern Portfolio Theory (MPT)**, **Machine Learning Risk Feature Scoring**, and **ARIMA Time-Series Forecasting**, the system calculates real-time volatility, detects single-asset risk drivers, simulates historical growth across custom timeframes, and projects future portfolio values with 95% confidence bounds.

---

## 🚀 Dual Workflow Operating Modes

When opening the platform, users can choose between two specialized operational workflows:
┌─────────────────────────────────────────────────────────────────────────────┐
│ SELECT WORKFLOW OPERATING MODE │
└──────────────────────────────┬──────────────────────────────┬───────────────┘
│ │
▼ ▼
┌──────────────────────────────────────────┐ ┌─────────────────────────────┐
│ 🆕 MODE 1: BUILD FROM SCRATCH │ │ ⚡ MODE 2: ENHANCE EXISTING │
├──────────────────────────────────────────┤ ├─────────────────────────────┤
│ • Input total investment capital ($) │ │ • Input custom stock tickers│
│ • Select target risk (Low/Medium/High) │ │ and percentage weights │
│ • Choose investment theme (Defensive, │ │ • Detect hidden risk driver │
│ Balanced Growth, Aggressive Innovation)│ │ assets & variance drivers │
│ • Auto-constructs optimized portfolio │ │ • Recommend optimal fund │
│ asset basket with profit/loss metrics │ │ redistribution weights │
└──────────────────────────────────────────┘ └─────────────────────────────┘

text


---

## 🏗️ System Architecture & Technology Stack

The platform utilizes a **decoupled 3-tier microservice architecture** designed for high throughput, low-latency vectorized calculations, and non-blocking database writes.
┌─────────────────────────────────────────────────────────────────────────────┐
│ FRONTEND (STREAMLIT) │
│ - Dual Workflow Mode Selector (Build Scratch vs. Enhance Existing) │
│ - Interactive Controls (Lookback 3m-2y, Forecast Horizon 7d-90d) │
│ - Plotly Visualizations (Risk Pie, Allocation Bar, Growth, ARIMA, Map) │
└──────────────────────────────────────┬──────────────────────────────────────┘
│ HTTP POST /analytics/evaluate
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ BACKEND (FASTAPI) │
│ - REST Routers (Analytics Engine, Market Ingestion, Portfolios) │
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
| **Frontend UI** | `Streamlit` | Reactive dashboard managing dynamic session state, workflow modes, and auto-updating visualizations. |
| **Data Visualization** | `Plotly Express` / `Graph Objects` | Render engine for Factor Risk, Re-allocation Comparison, Growth, and ARIMA CI Bands. |
| **Backend REST API** | `FastAPI` + `Uvicorn` | Asynchronous backend API engine executing financial pipelines and schema validation. |
| **Market Data** | `yfinance` | Vectorized batch fetching of historical daily prices aligned across global markets. |
| **Data Processing** | `pandas` + `numpy` | Linear algebra, covariance matrix computation, and daily return calculations. |
| **Machine Learning** | `scikit-learn` / Feature Scorer | Dynamic risk scoring (0–100) and risk tier categorization. |
| **Time-Series Forecast** | `statsmodels` (ARIMA) | ARIMA(1,1,1) model with trend drift for 7 to 90-day future portfolio path projections. |
| **Database & ORM** | `PostgreSQL` + `SQLAlchemy` | Relational persistence for Users, Portfolios, Allocations, and Market Data Cache. |
| **Test Suite** | `pytest` + `httpx` | 100% test-driven development (TDD) coverage across math services and API endpoints. |

---

## 🎯 Key Features Breakdown

### 1. Dual Portfolio Modes
* **Mode 1 (Build from Scratch):** Auto-constructs optimized baskets based on capital size, risk preference, and investment themes (*Balanced Growth*, *Defensive Preservation*, *Aggressive Tech*).
* **Mode 2 (Enhance Existing Portfolio):** Evaluates user-defined ticker allocations, flags dangerous concentration risk, and suggests weight redistribution.

### 2. Custom Historical Lookback Windows
* Flexible historical time-range analysis across **3 Months (`3m`)**, **6 Months (`6m`)**, **1 Year (`1y`)**, or **2 Years (`2y`)** to test performance across bull and bear regimes.

### 3. Net Profit / Loss Metrics
* Calculates net dollar profit/loss (`$`) and return on investment (`% ROI`) over selected historical lookback windows.

### 4. Quantitative & ML Risk Engine
* **Risk Score (0–100 Meter):** Computes a composite risk score combining Annual Volatility (50%), Max Drawdown (40%), and Concentration Penalty (10%).
* **Risk Categorization:** Classifies portfolios into `Low Risk`, `Medium Risk`, or `High Risk`.
* **Factor Risk Contribution:** Uses covariance matrix analysis to isolate which specific stock drives the highest variance.

### 5. Strategy Re-Allocation Engine
* Proposes optimal asset weight distribution smoothed toward equal-weighted baseline to achieve target risk goals.

### 6. Multi-Strategy Historical Backtesting
* Time-machine growth simulation comparing 4 concurrent strategies:
  1. **User Original Portfolio**
  2. **ML Recommended Allocation**
  3. **Equal-Weighted Strategy**
  4. **Market Benchmark** (S&P 500 `^GSPC`, NASDAQ-100 `^NDX`, NIFTY 50 `^NSEI`, or VT)

### 7. ARIMA Time-Series Forecasting
* Predicts expected portfolio growth over **7, 14, 30, 60, or 90 trading days**.
* Generates a **95% Confidence Interval band** (fan chart/funnel) modeling compounding market uncertainty over time.
* Connects the future projection line seamlessly to the recent 30-day historical actuals line.

### 8. Macro Stress-Testing & Risk-Return Map
* **Stress Test Engine:** Simulates capital impact during macroeconomic shocks (e.g., 2008 Financial Crisis -30%, Tech Crash -20%).
* **Risk vs. Return Map:** Plotly scatter map positioning individual assets on Volatility ($\sigma$) vs Return ($R$) axes.

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
│ fluctuations │ │ over past timeframe │ │ diversification │
└───────────────────────┘ └───────────────────────┘ └───────────────────────┘

text


#### 1. Annualized Volatility ($\sigma_{annual}$) — *Weight: 50%*
Calculates standard deviation of portfolio daily returns scaled across 252 annual trading days:

$$r_t = \frac{P_t - P_{t-1}}{P_{t-1}}, \quad R_{p,t} = \sum (r_{i,t} \cdot w_i)$$

$$\sigma_{annual} = \text{StdDev}(R_{p,t}) \times \sqrt{252}$$

$$\text{Vol\_Score} = \min\left(\frac{\sigma_{annual}}{0.35}, 1.0\right) \times 50$$

#### 2. Maximum Drawdown ($MDD$) — *Weight: 40%*
Evaluates worst peak-to-trough capital decline over the selected time window to measure downside loss risk:

$$V_t = \prod_{k=1}^{t} (1 + R_{p,k}), \quad \text{Peak}_t = \max_{1 \le k \le t} (V_k)$$

$$MDD = \max_{t} \left( \frac{\text{Peak}_t - V_t}{\text{Peak}_t} \right)$$

$$\text{MDD\_Score} = \min\left(\frac{MDD}{0.40}, 1.0\right) \times 40$$

#### 3. Concentration Penalty ($C$) — *Weight: 10%*
Penalizes portfolios for single-asset concentration:

$$\text{Penalty} = \max(0.0, 10.0 - (\text{Asset Count} \times 2.0))$$

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

#### 📈 Understanding the 95% Confidence Interval Band
* **Center Line:** Expected mean forecast baseline ($\hat{y}_t$).
* **Shaded Fan Band:** 95% Confidence bounds modeling compounding market volatility over time:

$$\text{Confidence Interval} = \hat{y}_t \pm 1.96 \times \text{SE}(\hat{y}_t)$$

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

## 🧪 Demo Test Data Sets (For Testing Mode 2)

Use these fresh ticker sets in Mode 2 to demonstrate different platform capabilities to judges:

| Test Scenario | Recommended Tickers & Allocations | Expected ML Risk Result |
| :--- | :--- | :--- |
| **High Volatility & Crypto** | `MSTR` (35%), `COIN` (25%), `PLTR` (20%), `META` (20%) | 🔴 **High Risk** (Score > 75) |
| **Defensive Preservation** | `KO` (30%), `JNJ` (30%), `WM` (20%), `TLT` (20%) | 🟢 **Low Risk** (Score < 30) |
| **Blue-Chip Financials** | `JPM` (30%), `XOM` (25%), `PG` (25%), `CAT` (20%) | 🟡 **Medium Risk** (Score ~45) |
| **Global & Commodities** | `TSM` (30%), `NVO` (25%), `SLV` (25%), `ASML` (20%) | 🟡 **Medium Risk** (Broad Beta) |

---

## ⚡ Setup & Execution Guide

### Prerequisites
* **Python:** Python 3.11
* **Database:** PostgreSQL (local or remote instance)

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/your-username/investment-risk-prediction.git
cd investment-risk-prediction

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
2. Configure Environment Variables
Create .env in the project root:

env

DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/investment_risk_db
TEST_DATABASE_URL=sqlite:///:memory:
3. Run Pytest Suite (TDD Verification)
Bash

PYTHONPATH=backend pytest -v
(All 21 unit and integration tests pass cleanly).

🚀 Running the Application
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
Web Dashboard: http://localhost:8501
📄 License
This project is open-source and available under the MIT License.






