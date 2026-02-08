"""Replicate AI for sentiment analysis (fast heuristic approach)."""

import os
from typing import Dict


def analyze_sentiment_replicate(price_data: dict) -> Dict:
    """
    Analyze sentiment using fast heuristic approach (no API calls - instant results).
    This is faster than waiting for Replicate API responses.
    
    Args:
        price_data: Dictionary with price and market data
    
    Returns:
        Dictionary with sentiment, confidence, and reasoning
    """
    try:
        # Simple heuristic-based approach that's instant and reliable
        change = price_data.get("change_24h", 0)
        high = price_data.get("high_24h", 0)
        low = price_data.get("low_24h", 0)
        current = price_data.get("current_price", 0)
        
        # Quick sentiment based on price movement
        if change > 5:
            sentiment = "BULLISH"
            confidence = min(10, 7 + (change / 10))
        elif change < -5:
            sentiment = "BEARISH"
            confidence = min(10, 7 + (abs(change) / 10))
        else:
            # Check if price is closer to high or low
            if current and high and low and (high - low) > 0:
                position = (current - low) / (high - low)
                if position > 0.65:
                    sentiment = "BULLISH"
                    confidence = 6
                elif position < 0.35:
                    sentiment = "BEARISH"
                    confidence = 6
                else:
                    sentiment = "NEUTRAL"
                    confidence = 5
            else:
                sentiment = "NEUTRAL"
                confidence = 5
        
        return {
            "available": True,
            "sentiment": sentiment,
            "confidence": round(confidence, 1),
            "reason": f"Based on 24h change: {change}%"
        }
    
    except Exception as e:
        return {
            "available": False,
            "error": f"Replicate error: {str(e)}"
        }
