import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

from src.indicators import compute_rsi, compute_bollinger, compute_macd
from src.metrics import compute_metrics

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LFC MarketView",
    page_icon="📈",
    layout="wide"
)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("LFC MarketView")
st.caption("LUISS Finance Club — IT & Quants Department")
st.divider()

# ─────────────────────────────────────────────
# SIDEBAR CONTROLS
# ─────────────────────────────────────────────
with st.sidebar:

    st.header("Controls")

    ticker = st.text_input(
        "Ticker",
        value="AAPL",
        help="Examples: AAPL, TSLA, SPY, BTC-USD"
    )

    timeframe = st.selectbox(
        "Timeframe",
        ["1mo","3mo","6mo","1y","2y","5y"],
        index=3
    )

    st.divider()

    st.header("Indicators")

    show_sma = st.checkbox("SMA (20 / 50)", True)
    show_bb = st.checkbox("Bollinger Bands", False)
    show_rsi = st.checkbox("RSI (14)", False)
    show_macd = st.checkbox("MACD (12,26,9)", False)

    st.divider()

    if st.button("Refresh Data", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data(ticker, period):

    df = yf.download(
        ticker,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False
    )

    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

    return df


data = load_data(ticker, timeframe)

if data.empty:
    st.error("No data found. Try AAPL, TSLA, SPY, BTC-USD")
    st.stop()

# ─────────────────────────────────────────────
# COMPUTE METRICS
# ─────────────────────────────────────────────
metrics = compute_metrics(data, ticker)

# ─────────────────────────────────────────────
# DYNAMIC CHART STRUCTURE
# ─────────────────────────────────────────────
rows = 2
row_heights = [0.6, 0.15]

if show_rsi:
    rows += 1
    row_heights.append(0.125)

if show_macd:
    rows += 1
    row_heights.append(0.125)

fig = make_subplots(
    rows=rows,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=row_heights
)

price_row = 1
volume_row = 2
current_row = 3

# ─────────────────────────────────────────────
# PRICE (CANDLESTICKS)
# ─────────────────────────────────────────────
fig.add_trace(
    go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Price",
        increasing_line_color="#00cc88",
        decreasing_line_color="#ff4444"
    ),
    row=price_row,
    col=1
)

# ─────────────────────────────────────────────
# SMA
# ─────────────────────────────────────────────
if show_sma:

    data["SMA20"] = data["Close"].rolling(20).mean()
    data["SMA50"] = data["Close"].rolling(50).mean()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["SMA20"],
            name="SMA 20",
            line=dict(color="orange", width=1.5)
        ),
        row=price_row,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["SMA50"],
            name="SMA 50",
            line=dict(color="royalblue", width=1.5)
        ),
        row=price_row,
        col=1
    )

# ─────────────────────────────────────────────
# BOLLINGER BANDS
# ─────────────────────────────────────────────
if show_bb:

    upper, lower = compute_bollinger(data)

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=upper,
            name="BB Upper",
            line=dict(color="gray", width=1)
        ),
        row=price_row,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=lower,
            name="BB Lower",
            line=dict(color="gray", width=1),
            fill="tonexty",
            fillcolor="rgba(128,128,128,0.15)"
        ),
        row=price_row,
        col=1
    )

# ─────────────────────────────────────────────
# VOLUME
# ─────────────────────────────────────────────
volume_colors = np.where(
    data["Close"] >= data["Open"],
    "#00cc88",
    "#ff4444"
)

fig.add_trace(
    go.Bar(
        x=data.index,
        y=data["Volume"],
        name="Volume",
        marker_color=volume_colors,
        opacity=0.7
    ),
    row=volume_row,
    col=1
)

# ─────────────────────────────────────────────
# RSI
# ─────────────────────────────────────────────
if show_rsi:

    data["RSI"] = compute_rsi(data)

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["RSI"],
            name="RSI (14)",
            line=dict(color="purple", width=2)
        ),
        row=current_row,
        col=1
    )

    fig.add_hline(y=70, line_dash="dash", line_color="red", row=current_row, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=current_row, col=1)

    fig.update_yaxes(range=[0,100], row=current_row, col=1)

    current_row += 1

# ─────────────────────────────────────────────
# MACD
# ─────────────────────────────────────────────
if show_macd:

    data["MACD"], data["MACD_SIGNAL"], data["MACD_HIST"] = compute_macd(data)

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["MACD"],
            name="MACD",
            line=dict(color="cyan", width=2)
        ),
        row=current_row,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["MACD_SIGNAL"],
            name="Signal",
            line=dict(color="orange", width=2)
        ),
        row=current_row,
        col=1
    )

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["MACD_HIST"],
            name="Histogram",
            marker_color="gray",
            opacity=0.5
        ),
        row=current_row,
        col=1
    )

# ─────────────────────────────────────────────
# CHART LAYOUT
# ─────────────────────────────────────────────
fig.update_layout(
    title=f"{ticker.upper()} · {timeframe}",
    template="plotly_dark",
    height=900,
    hovermode="x unified",
    xaxis_rangeslider_visible=False,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# ─────────────────────────────────────────────
# RENDER CHART
# ─────────────────────────────────────────────
st.plotly_chart(
    fig,
    use_container_width=True,
    key="market_chart"
)

st.divider()

# ─────────────────────────────────────────────
# LIVE QUANT METRICS
# ─────────────────────────────────────────────
st.subheader("Live Quant Metrics")

latest_rsi = None
if "RSI" in data.columns:
    latest_rsi = round(data["RSI"].iloc[-1],2)

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Sharpe Ratio", f"{metrics['sharpe']:.2f}")
m2.metric("Volatility", f"{metrics['volatility']*100:.2f}%")
m3.metric("RSI (14)", latest_rsi if latest_rsi else "—")
m4.metric("Beta vs SPY", f"{metrics['beta']:.2f}")
m5.metric("Max Drawdown", f"{metrics['max_drawdown']*100:.2f}%")

st.divider()

# ─────────────────────────────────────────────
# RAW DATA TABLE
# ─────────────────────────────────────────────
with st.expander("View Raw Data (last 20 days)"):

    st.dataframe(
        data.tail(20),
        use_container_width=True
    )

st.divider()

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.caption(
    "Data: Yahoo Finance via yfinance · Built for LUISS Finance Club"
)