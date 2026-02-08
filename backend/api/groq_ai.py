"""Groq API integration - instant heuristic for speed."""

import os
from typing import Optional, Dict


def analyze_sentiment_groq(market_data: Dict, api_key: Optional[str] = None) -> Dict:
    """
    Instant sentiment analysis using heuristic (no API delays).
    
    Args:
        market_data: Dictionary with price data
    
    Returns:
        Dictionary with sentiment analysis
    """
    change = market_data.get('change_24h', 0)
    high = market_data.get('high_24h', 0)
    low = market_data.get('low_24h', 0)
    current = market_data.get('current_price', 0)
    
    # Quick analysis
    if change > 4:
        sentiment = "BUY"
        confidence = min(10, 7 + (change / 10))
    elif change < -4:
        sentiment = "SELL"
        confidence = min(10, 7 + (abs(change) / 10))
    else:
        if current and high and low and (high - low) > 0:
            position = (current - low) / (high - low)
            if position > 0.6:
                sentiment = "BUY"
                confidence = 6
            elif position < 0.4:
                sentiment = "SELL"
                confidence = 6
            else:
                sentiment = "HOLD"
                confidence = 5
        else:
            sentiment = "HOLD"
            confidence = 5
    
    return {
        "available": True,
        "sentiment": sentiment,
        "confidence": round(confidence, 1)
    }
