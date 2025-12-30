import yfinance as yf
import pandas as pd


# ---------- SAFETY HELPER ----------
def to_float(x):
    try:
        return float(x)
    except Exception:
        return None


# ---------- PRICE DATA ----------
def get_price_data(symbol):
    df = yf.download(symbol, period="6mo", interval="1d")
    df.dropna(inplace=True)
    return df


# ---------- RSI ----------
def compute_rsi(close, window=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return to_float(rsi.iloc[-1])


# ---------- MOVING AVERAGES ----------
def compute_moving_averages(close):
    ma50 = to_float(close.rolling(50).mean().iloc[-1])
    ma200 = to_float(close.rolling(200).mean().iloc[-1])
    return ma50, ma200


# ---------- MACD ----------
def compute_macd(close):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return to_float(macd.iloc[-1]), to_float(signal.iloc[-1])


# ---------- BOLLINGER BANDS ----------
def compute_bollinger_bands(close, window=20):
    sma = close.rolling(window).mean()
    std = close.rolling(window).std()
    upper = to_float((sma + 2 * std).iloc[-1])
    lower = to_float((sma - 2 * std).iloc[-1])
    return upper, lower


# ---------- VOLUME TREND ----------
def compute_volume_trend(volume):
    recent = to_float(volume.tail(5).mean())
    previous = to_float(volume.tail(20).mean())

    if None in (recent, previous):
        return "Unknown"
    if recent > previous:
        return "Increasing"
    elif recent < previous:
        return "Decreasing"
    return "Stable"


# ---------- TREND DIRECTION ----------
def determine_trend(close, ma50, ma200):
    price = to_float(close.iloc[-1])

    if None in (price, ma50, ma200):
        return "Unknown"

    if price > ma50 and ma50 > ma200:
        return "Strong Uptrend"
    elif price < ma50 and ma50 < ma200:
        return "Strong Downtrend"
    return "Sideways / Unclear"


# ---------- FUNDAMENTAL RATIOS ----------
def get_fundamental_ratios(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info

    return {
        "Revenue Growth": info.get("revenueGrowth"),
        "Net Profit Margin": info.get("profitMargins"),
        "Debt to Equity": info.get("debtToEquity"),
        "Current Ratio": info.get("currentRatio"),
        "Return on Equity": info.get("returnOnEquity"),
        "Free Cash Flow": info.get("freeCashflow"),
    }
