"""Google Gemini AI integration for market sentiment analysis."""

import os
import json
from typing import Optional, Dict

try:
    import google.generativeai as genai
except ImportError:
    genai = None


def initialize_gemini(api_key: Optional[str] = None) -> bool:
    """
    Initialize Gemini API with API key.
    
    Args:
        api_key: Google Gemini API key (or from GEMINI_API_KEY env var)
    
    Returns:
        True if initialized successfully
    """
    if not genai:
        print("google-generativeai not installed")
        return False
    
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        print("No Gemini API key provided")
        return False
    
    genai.configure(api_key=key)
    return True


def analyze_trading_pair(pair_name: str, price_data: Dict) -> Dict:
    """
    Use Gemini to analyze a trading pair and generate trading signals.
    
    Args:
        pair_name: Cryptocurrency pair name (e.g., "Bitcoin")
        price_data: Dictionary with current_price, change_24h, market_cap, volume_24h
    
    Returns:
        Dictionary with sentiment, signal, and explanation
    """
    if not genai:
        result = _mock_analysis(pair_name, price_data)
        result["available"] = True
        return result
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        
        prompt = f"Analyze {pair_name} at ${price_data.get('current_price')} (24h change: {price_data.get('change_24h')}%). Respond JSON: {{'sentiment': 'Bullish/Neutral/Bearish', 'signal': 'BUY/HOLD/SELL', 'confidence': 1-10}}"
        
        response = model.generate_content(prompt, request_options={"timeout": 4})
        
        # Parse response
        try:
            result = json.loads(response.text)
            result["available"] = True
            return result
        except:
            result = _mock_analysis(pair_name, price_data)
            result["available"] = True
            return result
    
    except Exception as e:
        result = _mock_analysis(pair_name, price_data)
        result["available"] = True
        return result


def _mock_analysis(pair_name: str, price_data: Dict) -> Dict:
    """Generate mock analysis when API is unavailable."""
    change = price_data.get('change_24h', 0)
    
    if change > 5:
        sentiment = "Bullish"
        signal = "BUY"
        confidence = 7
    elif change < -5:
        sentiment = "Bearish"
        signal = "SELL"
        confidence = 6
    else:
        sentiment = "Neutral"
        signal = "HOLD"
        confidence = 5
    
    return {
        "sentiment": sentiment,
        "signal": signal,
        "confidence": confidence,
        "explanation": f"Based on 24h change of {change:.2f}%. Mock analysis (API not available)."
    }
