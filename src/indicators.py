def compute_rsi(data, window=14):

    delta = data["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window).mean() # Calculate the average gain over the specified window
    avg_loss = loss.rolling(window).mean() # Calculate the average loss over the specified window

    rs = avg_gain / avg_loss # Calculate the Relative Strength (RS) by dividing the average gain by the average loss

#RSI measures the strength of a stock's price action by comparing the magnitude of recent gains to recent losses.  
#The resulting RSI value ranges from 0 to 100, with values above 70 typically indicating overbought conditions and values below 30 indicating oversold conditions.
    
    rsi = 100 - (100 / (1 + rs)) 

    return rsi

# ─────────────────────────────────────────────
# BOLLINGER BANDS FUNCTION
# ─────────────────────────────────────────────
def compute_bollinger(data, window=20):

    sma = data["Close"].rolling(window).mean()
    std = data["Close"].rolling(window).std()

    upper_band = sma + (2 * std)
    lower_band = sma - (2 * std)

    return upper_band, lower_band

def compute_macd(data):

    ema12 = data["Close"].ewm(span=12, adjust=False).mean()
    ema26 = data["Close"].ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    histogram = macd - signal

    return macd, signal, histogram