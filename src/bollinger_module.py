# ─────────────────────────────────────────────
# BOLLINGER BANDS FUNCTION
# ─────────────────────────────────────────────
def compute_bollinger(data, window=20):

    sma = data["Close"].rolling(window).mean()
    std = data["Close"].rolling(window).std()

    upper_band = sma + (2 * std)
    lower_band = sma - (2 * std)

    return sma, upper_band, lower_band