from analysis import *
from agents import *


def run_analysis(symbol):
    price_data = get_price_data(symbol)
    close = price_data["Close"]

    rsi = compute_rsi(close)
    ma50, ma200 = compute_moving_averages(close)
    macd, macd_signal = compute_macd(close)
    bb_upper, bb_lower = compute_bollinger_bands(close)
    volume_trend = compute_volume_trend(price_data["Volume"])
    trend = determine_trend(close, ma50, ma200)

    ratios = get_fundamental_ratios(symbol)

    technicals = {
        "RSI": rsi,
        "MA50": ma50,
        "MA200": ma200,
        "MACD": macd,
        "MACD Signal": macd_signal,
        "Bollinger Upper": bb_upper,
        "Bollinger Lower": bb_lower,
        "Volume Trend": volume_trend,
        "Trend Direction": trend
    }

    fundamental = fundamental_analyst_agent(ratios)
    management = management_quality_agent()
    technical = technical_analyst_agent(technicals)
    contrarian = contrarian_agent()

    final_decision = chairman_agent(
        fundamental, management, technical, contrarian
    )

    return {
        "Fundamental Analysis": fundamental,
        "Management Analysis": management,
        "Technical Analysis": technical,
        "Contrarian View": contrarian,
        "Final Decision": final_decision
    }
