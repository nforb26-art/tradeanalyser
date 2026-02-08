"""Trading analysis logic for entry, stoploss, and take profit calculation."""

def calculate_volatility(high_24h: float, low_24h: float, current_price: float) -> float:
    """
    Calculate volatility percentage based on 24h range.
    
    Args:
        high_24h: 24-hour high price
        low_24h: 24-hour low price
        current_price: Current price
    
    Returns:
        Volatility percentage (0-100+)
    """
    if current_price == 0:
        return 0
    
    price_range = high_24h - low_24h
    volatility = (price_range / current_price) * 100
    return volatility


def calculate_analysis(price_data: dict) -> dict:
    """
    Calculate entry point, stop loss, and take profit based on price data and market volatility.
    
    Args:
        price_data: Dictionary with current_price, high_24h, low_24h, change_24h
    
    Returns:
        Dictionary with entry, stoploss, takeprofit, and analysis details
    """
    current = price_data.get("current_price", 0)
    high_24 = price_data.get("high_24h", current)
    low_24 = price_data.get("low_24h", current)
    change_24 = price_data.get("change_24h", 0)
    
    if current == 0:
        return {
            "entry": None,
            "stoploss": None,
            "takeprofit": None,
            "error": "Invalid price data - current price is 0"
        }
    
    # Calculate volatility
    volatility = calculate_volatility(high_24, low_24, current)
    
    # Entry: use current price
    entry = current
    
    # Dynamic Stop Loss based on volatility
    # Higher volatility = wider stop loss
    # Low volatility (< 2%): 1.5% SL
    # Medium volatility (2-5%): 2.5% SL
    # High volatility (5-10%): 4% SL
    # Very high volatility (> 10%): 6% SL
    
    if volatility < 2:
        sl_percentage = 1.5
    elif volatility < 5:
        sl_percentage = 2.5
    elif volatility < 10:
        sl_percentage = 4.0
    else:
        sl_percentage = 6.0
    
    stoploss = current * (1 - sl_percentage / 100)
    
    # Take profit: adjusted by trend and volatility
    # Base TP: 5%
    # Uptrend (+5% change): add 2-3%
    # Downtrend (-5% change): reduce to 2%
    # Volatility adjustment: +1% per 5% volatility
    
    base_tp = 5.0
    
    if change_24 > 5:
        tp_percentage = base_tp + 3.0
    elif change_24 > 0:
        tp_percentage = base_tp + (change_24 / 5.0)
    elif change_24 > -5:
        tp_percentage = base_tp - 2.0
    else:
        tp_percentage = base_tp - 3.0
    
    # Add volatility adjustment (safer on high volatility)
    volatility_adjustment = min(2.0, volatility / 5.0)
    if change_24 < 0:
        tp_percentage += volatility_adjustment
    
    takeprofit = current * (1 + tp_percentage / 100)
    
    return {
        "entry": round(entry, 8),
        "stoploss": round(stoploss, 8),
        "takeprofit": round(takeprofit, 8),
        "analysis_basis": {
            "high_24h": high_24,
            "low_24h": low_24,
            "change_24h": change_24,
            "volatility": round(volatility, 2),
            "volatility_level": classify_volatility(volatility)
        },
        "sl_percentage": round(sl_percentage, 2),
        "tp_percentage": round(tp_percentage, 2)
    }


def classify_volatility(volatility: float) -> str:
    """Classify volatility level."""
    if volatility < 2:
        return "VERY LOW"
    elif volatility < 5:
        return "LOW"
    elif volatility < 10:
        return "MEDIUM"
    elif volatility < 15:
        return "HIGH"
    else:
        return "EXTREME"


def apply_sentiment_adjustment(analysis: dict, sentiment_score: float) -> dict:
    """
    Adjust analysis based on AI sentiment score (-1 to 1).
    
    Args:
        analysis: Base analysis dict
        sentiment_score: Score from -1 (bearish) to 1 (bullish)
    
    Returns:
        Adjusted analysis
    """
    if sentiment_score > 0.5:  # Bullish
        adjustment = 1 + (0.02 * sentiment_score)
        analysis["takeprofit"] = round(analysis["takeprofit"] * adjustment, 8)
    elif sentiment_score < -0.5:  # Bearish
        adjustment = 1 - (0.02 * abs(sentiment_score))
        analysis["stoploss"] = round(analysis["stoploss"] * adjustment, 8)
    
    return analysis
