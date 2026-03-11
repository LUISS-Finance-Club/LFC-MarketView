import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Cesar's TODOs Week 1:
# - [x] Set up Streamlit page and sidebar controls
# - [x] Load historical price data with yfinance
# - [x] Plot candlestick chart with Plotly
# - [x] Add SMA 20 & 50 (Part 1)



# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LFC MarketView",
    page_icon="LOGO",
    layout="wide"
)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("LFC MarketView")
st.caption("LUISS Finance Club — IT & Quants Department")
st.divider()

# ─────────────────────────────────────────────
# SIDEBAR — CONTROLS
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("Controls")

    ticker = st.text_input("Ticker", value="AAPL", help="e.g. AAPL, SPY, BTC-USD, TSLA")
    timeframe = st.selectbox(
        "Timeframe",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3
    )

    st.divider()

    st.header("Indicators")
    st.caption("Toggle on/off — code these in Week 2 & 3")

    show_sma   = st.checkbox("SMA  (20 / 50)",     value=True)
    show_rsi   = st.checkbox("RSI  (14)",           value=False)
    show_bb    = st.checkbox("Bollinger Bands",     value=False)
    show_macd  = st.checkbox("MACD (12, 26, 9)",   value=False)

    st.divider()

    if st.button("Refresh Data", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.divider()

    # ── CESAR'S PROGRESS CHECKLIST ──
    st.header("Your Progress")
    st.markdown("""
- [x] **Week 1** — Candlesticks + SMA
- [ ] **Week 2** — RSI + Bollinger
- [ ] **Week 3** — MACD + Real Metrics
- [ ] **Deploy** — Vercel / Streamlit Cloud
    """)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data(ticker: str, period: str) -> pd.DataFrame:
    df = yf.download(ticker, period=period, interval="1d", progress=False, auto_adjust=True)
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    return df

data = load_data(ticker, timeframe)

if data.empty:
    st.error("No data found. Try AAPL, SPY, BTC-USD, TSLA")
    st.stop()

# ─────────────────────────────────────────────
# MAIN CHART — CANDLESTICKS (TEMPLATE PROVIDES)
# ─────────────────────────────────────────────
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    name="Price",
    increasing_line_color="#00cc88",
    decreasing_line_color="#ff4444",
))

# RSI computation function
# ─────────────────────────────────────────────
# RSI FUNCTION
# ─────────────────────────────────────────────
# import the compute_rsi function from the rsi_module.py file
from src.rsi_module import compute_rsi
# ─────────────────────────────────────────────
# DUMMY SMA —  REPLACE IN PART 1
# ─────────────────────────────────────────────
if show_sma:
    sma20 = data["Close"].rolling(20).mean()
    sma50 = data["Close"].rolling(50).mean()
    fig.add_trace(go.Scatter(x=data.index, y=sma20, name="SMA 20",
                             line=dict(color="orange", width=1.5)))
    fig.add_trace(go.Scatter(x=data.index, y=sma50, name="SMA 50",
                             line=dict(color="royalblue", width=1.5)))

# ─────────────────────────────────────────────
# PLACEHOLDERS — ADD THESE
# ─────────────────────────────────────────────
if show_rsi:
    st.info("Code RSI(14): Updates pending this week..")
    # Coding the RSI by calling the compute_rsi function and plotting it.
    data["RSI"] = compute_rsi(data) 


    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["RSI"],
            name="RSI (14)",
            line=dict(color="purple", width=2)
        )
    )

    # Overbought line
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought", annotation_position="top left")

    # Oversold line
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold", annotation_position="bottom left")

    # fig.update_layout(
    #     title="RSI (Relative Strength Index)",
    #     template="plotly_dark",
    #     height=400,
    #     yaxis_title="RSI"
    # )

    # st.plotly_chart(fig, use_container_width=True)
    
if show_bb:
    st.info("PART 2 TODO: Code Bollinger Bands (SMA20 ± 2σ) and add to chart")

if show_macd:
    st.info("PART 3 TODO: Code MACD (EMA12 - EMA26) + signal line + histogram")

# ─────────────────────────────────────────────
# CHART LAYOUT
# ─────────────────────────────────────────────
fig.update_layout(
    title=f"{ticker.upper()}   ·   {timeframe}",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    height=560,
    template="plotly_dark",
    hovermode="x unified",
    xaxis_rangeslider_visible=False,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# LIVE METRICS ROW — DUMMY VALUES
# REPLACE WITH REAL FORMULAS IN PART 3
# ─────────────────────────────────────────────
st.subheader("Live Quant Metrics")
st.caption("Currently showing dummy values — replace with real formulas in Part 3")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Sharpe Ratio",    "1.23",   help="(Annualised return - Rf) / σ")
m2.metric("Volatility",      "24.1%",  help="Annualised std dev of daily returns")
m3.metric("RSI (14)",        "68",     help="Relative Strength Index")
m4.metric("Beta",            "1.12",   help="Covariance(asset, SPY) / Variance(SPY)")
m5.metric("Max Drawdown",    "-12.3%", help="Largest peak-to-trough decline")

st.divider()

# ─────────────────────────────────────────────
# RAW DATA TABLE
# ─────────────────────────────────────────────
with st.expander("View Raw Data (last 20 rows)"):
    st.dataframe(data.tail(20), use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.caption("Data: Yahoo Finance via yfinance · Template by LUISS Finance Club IT & Quants Department")
