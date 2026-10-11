import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from typing import Dict, Any

st.set_page_config(
    page_title="Investment Risk & Portfolio Optimization Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = "http://127.0.0.1:8000"

st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Investment Risk Prediction & Portfolio Optimization")
st.caption("Real-Time yFinance Market Data, Dynamic Auto-Updating ML Risk Engine")

# --- SIDEBAR INPUTS ---
st.sidebar.header("🛠️ Portfolio Setup")

user_id = st.sidebar.text_input("User ID", value="default_user")
total_investment = st.sidebar.number_input("Total Investment ($)", min_value=100.0, value=10000.0, step=500.0)
target_risk_input = st.sidebar.selectbox("Target Risk Level Preference", ["Low", "Medium", "High"], index=1)
benchmark_ticker = st.sidebar.selectbox(
    "Market Benchmark Comparison", 
    ["^GSPC", "^NDX", "^NSEI", "VT"], 
    format_func=lambda x: {"^GSPC": "S&P 500 (^GSPC)", "^NDX": "NASDAQ-100 (^NDX)", "^NSEI": "NIFTY 50 (^NSEI)", "VT": "Vanguard Total World (VT)"}[x]
)

st.sidebar.subheader("Asset Allocations")
st.sidebar.write("Specify asset tickers and their allocations (%)")

DEFAULT_PRESETS = [
    {"ticker": "AAPL", "weight": 30.0},
    {"ticker": "MSFT", "weight": 25.0},
    {"ticker": "TSLA", "weight": 20.0},
    {"ticker": "BND", "weight": 15.0},
    {"ticker": "GOOGL", "weight": 10.0},
    {"ticker": "AMZN", "weight": 0.0},
    {"ticker": "NVDA", "weight": 0.0},
    {"ticker": "SPY", "weight": 0.0},
    {"ticker": "QQQ", "weight": 0.0},
    {"ticker": "GLD", "weight": 0.0},
]

num_assets = st.sidebar.number_input("Number of Assets", min_value=1, max_value=10, value=5)

allocations = {}
seen_tickers = []
has_duplicate = False

for i in range(int(num_assets)):
    preset = DEFAULT_PRESETS[i] if i < len(DEFAULT_PRESETS) else {"ticker": f"ASSET{i+1}", "weight": 0.0}
    
    col_t, col_w = st.sidebar.columns([1, 1])
    ticker = col_t.text_input(f"Ticker {i+1}", value=preset["ticker"], key=f"t_{i}").upper().strip()
    weight = col_w.number_input(f"Weight % {i+1}", min_value=0.0, max_value=100.0, value=preset["weight"], step=5.0, key=f"w_{i}")
    
    if ticker:
        if ticker in seen_tickers:
            has_duplicate = True
        else:
            seen_tickers.append(ticker)
        allocations[ticker] = weight / 100.0

total_weight_pct = sum(allocations.values()) * 100.0

if has_duplicate:
    st.sidebar.error("⚠️ Duplicate tickers detected! Please ensure each asset ticker is unique.")

if abs(total_weight_pct - 100.0) > 0.01:
    st.sidebar.warning(f"⚠️ Allocations must sum to 100%. Current sum: **{total_weight_pct:.1f}%**")
else:
    st.sidebar.success("✅ Allocations equal 100%")

force_reload = st.sidebar.button("🔄 Force Refresh Graphs", type="primary", use_container_width=True)

def fetch_portfolio_analytics(alloc_dict: Dict[str, float], target_risk: str, bench: str) -> Any:
    try:
        res = requests.post(
            f"{BACKEND_URL}/analytics/evaluate",
            json={"allocations": alloc_dict, "target_risk": target_risk, "benchmark": bench},
            timeout=15
        )
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Backend API Error: {res.json().get('detail', res.text)}")
            return None
    except Exception as e:
        st.error(f"Failed to connect to backend server at {BACKEND_URL}. Ensure FastAPI is running! Error: {e}")
        return None

current_input_state = {
    "allocations": allocations,
    "target_risk": target_risk_input,
    "benchmark": benchmark_ticker,
    "total_investment": total_investment,
    "valid": (not has_duplicate) and (abs(total_weight_pct - 100.0) <= 0.01)
}

# Clear stale memory if graph fields are missing
if "analytics_data" in st.session_state:
    if "historical_growth" not in st.session_state.analytics_data or force_reload:
        del st.session_state["analytics_data"]
        if "last_input_state" in st.session_state:
            del st.session_state["last_input_state"]

if current_input_state["valid"]:
    if st.session_state.get("last_input_state") != current_input_state or "analytics_data" not in st.session_state:
        with st.spinner("🔄 Fetching real market data & calculating historical growth simulation..."):
            analytics = fetch_portfolio_analytics(allocations, target_risk_input, benchmark_ticker)
            if analytics:
                st.session_state.analytics_data = analytics
                st.session_state.active_allocations = allocations
                st.session_state.last_input_state = current_input_state
            else:
                st.stop()

# --- MAIN DISPLAY CONTENT ---
if "analytics_data" in st.session_state and current_input_state["valid"]:
    analytics = st.session_state.analytics_data
    active_allocs = st.session_state.active_allocations

    # 1. TOP METRICS DASHBOARD
    st.subheader("📊 Live Key Performance & Risk Metrics")
    
    m1, m2, m3, m4, m5 = st.columns(5)
    risk_color = "🟢" if analytics["risk_level"] == "Low" else ("🟡" if analytics["risk_level"] == "Medium" else "🔴")
    
    m1.metric("ML Risk Level", f"{risk_color} {analytics['risk_level']}")
    m2.metric("Risk Score", f"{analytics['risk_score']:.1f} / 100")
    m3.metric("Annual Volatility", f"{analytics['annualized_volatility'] * 100:.2f}%")
    m4.metric("Max Drawdown (MDD)", f"{analytics['max_drawdown'] * 100:.2f}%")
    m5.metric("Sharpe Ratio", f"{analytics['sharpe_ratio']:.2f}")

    st.info(f"💡 **ML Risk Classification Reasoning:** {analytics['explanation']}")

    if "ai_market_intelligence" in analytics:
        ai_data = analytics["ai_market_intelligence"]
        with st.expander("🤖 **AI Qualitative Intelligence & Market Outlook**", expanded=True):
            st.markdown(f"### {ai_data['headline']}")
            for bullet in ai_data["insights"]:
                st.markdown(f"- {bullet}")
    
    st.divider()

    # 2. FACTOR RISK CONTRIBUTION & ALLOCATION COMPARISON
    c1, c2 = st.columns([1, 1])

    with c1:
        st.subheader("🎯 Factor Risk Contribution")
        st.caption("Identifies which asset drives the highest risk variance in the real market")
        
        risk_df = pd.DataFrame([
            {"Asset": ticker, "Risk Contribution (%)": weight * 100.0} 
            for ticker, weight in analytics["risk_contributions"].items()
        ])
        
        fig_risk = px.pie(
            risk_df, 
            values="Risk Contribution (%)", 
            names="Asset", 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_risk.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_risk, use_container_width=True)

    with c2:
        st.subheader("⚖️ Portfolio Re-Allocation Recommendation")
        st.caption(f"Suggested asset weights to target **{target_risk_input}** risk profile")
        
        rec_data = []
        for ticker in active_allocs.keys():
            rec_data.append({
                "Asset": ticker,
                "Current Allocation": active_allocs[ticker] * 100.0,
                "Recommended Allocation": analytics["recommended_allocation"].get(ticker, 0.0) * 100.0
            })
        rec_df = pd.DataFrame(rec_data)
        
        fig_alloc = px.bar(
            rec_df, 
            x="Asset", 
            y=["Current Allocation", "Recommended Allocation"],
            barmode="group",
            labels={"value": "Weight (%)", "variable": "Strategy"},
            color_discrete_sequence=["#3366CC", "#109618"]
        )
        fig_alloc.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_alloc, use_container_width=True)

    st.divider()

    # 3. HISTORICAL SIMULATION & STRATEGY COMPARISON
    st.subheader("📈 Multi-Strategy Real Historical Growth Simulation")
    st.caption("1-Year historical value ($): User Portfolio vs Recommended Allocation vs Equal Weight vs Benchmark")

    if "historical_growth" in analytics and analytics["historical_growth"]:
        growth_df = pd.DataFrame(analytics["historical_growth"])
        growth_df["date"] = pd.to_datetime(growth_df["date"])
        growth_df = growth_df.set_index("date")
        
        # Multiply ratio curve by actual total investment dollar amount
        for col in growth_df.columns:
            growth_df[col] = growth_df[col] * total_investment

        fig_growth = px.line(
            growth_df, 
            labels={"value": "Portfolio Value ($)", "date": "Date"},
            color_discrete_map={
                "User Original Portfolio": "#FF9900",
                "ML Recommended Allocation": "#00CC96",
                "Equal Weighted Portfolio": "#AB63FA",
                f"Benchmark ({benchmark_ticker})": "#EF553B"
            }
        )
        fig_growth.update_layout(
            hovermode="x unified", 
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_growth, use_container_width=True)
    else:
        st.warning("⚠️ Historical growth simulation data is loading...")

    st.divider()

    # 4. MARKET SCENARIO STRESS TESTING & RISK-RETURN SCATTER
    col_st, col_sc = st.columns([1, 1])

    with col_st:
        st.subheader("⚡ Market Scenario Stress-Test Engine")
        st.caption("Simulate portfolio capital drawdown under stress events")
        
        scenario = st.selectbox(
            "Select Stress Test Scenario",
            [
                "Custom Shock",
                "2008 Financial Crisis (-30% Drop)",
                "Tech Sector Downturn (-20% Drop)",
                "High Volatility Inflation Shock (-15% Drop)"
            ]
        )
        
        if scenario == "2008 Financial Crisis (-30% Drop)":
            shock_val = -30.0
        elif scenario == "Tech Sector Downturn (-20% Drop)":
            shock_val = -20.0
        elif scenario == "High Volatility Inflation Shock (-15% Drop)":
            shock_val = -15.0
        else:
            shock_val = st.slider("Simulated Market Drawdown Drop (%)", min_value=-50.0, max_value=0.0, value=-10.0, step=1.0)
            
        simulated_val = total_investment * (1.0 + (shock_val / 100.0))
        simulated_loss = total_investment - simulated_val
        
        st.warning(f"📉 Under **{scenario}**, estimated portfolio value changes to **${simulated_val:,.2f}** (Loss: **-${simulated_loss:,.2f}** / **{shock_val:.1f}%**)")

    with col_sc:
        st.subheader("🎯 Risk vs. Return Asset Map")
        st.caption("Visualizing individual asset performance coordinates")
        
        if "asset_stats" in analytics and analytics["asset_stats"]:
            scatter_records = []
            for asset_name, stats in analytics["asset_stats"].items():
                scatter_records.append({
                    "Asset": asset_name,
                    "Expected Return (%)": stats["return_pct"],
                    "Annual Volatility (%)": stats["volatility_pct"]
                })
            scatter_df = pd.DataFrame(scatter_records)
            
            fig_scatter = px.scatter(
                scatter_df,
                x="Annual Volatility (%)",
                y="Expected Return (%)",
                text="Asset",
                size=[14]*len(scatter_df),
                color="Asset"
            )
            fig_scatter.update_traces(textposition='top center')
            fig_scatter.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.info("👈 Enter your asset allocations in the sidebar to begin real-time analysis!")
