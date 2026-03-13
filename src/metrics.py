import pandas as pd
import numpy as np
import yfinance as yf


def compute_metrics(df, ticker):

    returns = df["Close"].pct_change().dropna()

    # Annualized volatility
    volatility = returns.std() * np.sqrt(252)

    # Sharpe Ratio (Rf assumed 0 for simplicity)
    sharpe = (returns.mean() * 252) / volatility

    # Max Drawdown
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    # Beta vs SPY
    spy = yf.download("SPY", period="5y", interval="1d", progress=False)
    spy_returns = spy["Close"].pct_change().dropna()

    combined = pd.concat([returns, spy_returns], axis=1).dropna()
    combined.columns = ["asset", "spy"]

    covariance = np.cov(combined["asset"], combined["spy"])[0][1]
    spy_var = np.var(combined["spy"])

    beta = covariance / spy_var

    return {
        "sharpe": sharpe,
        "volatility": volatility,
        "beta": beta,
        "max_drawdown": max_drawdown
    }