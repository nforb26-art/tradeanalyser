"""Alpha Vantage API integration for technical indicators (free tier available)."""

import requests
import os
from typing import Optional, Dict

ALPHAVANTAGE_BASE = "https://www.alphavantage.co/query"


def initialize_alphavantage(api_key: Optional[str] = None) -> str:
    """Get Alpha Vantage key from parameter or environment."""
    return api_key or os.getenv("ALPHAVANTAGE_KEY", "demo")


def get_intraday_data(symbol: str, api_key: Optional[str] = None) -> Optional[Dict]:
    """
    Get intraday price data and simple technical indicators.
    Note: Alpha Vantage requires a specific stock/forex symbol format.
    
    Args:
        symbol: Trading symbol (e.g., "BTC/USD" format won't work; use "EURUSD")
        api_key: Alpha Vantage API key
    
    Returns:
        Dictionary with price data and indicators
    """
    key = initialize_alphavantage(api_key)
    
    try:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "60min",
            "apikey": key
        }
        
        response = requests.get(ALPHAVANTAGE_BASE, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Check for errors
        if "Error Message" in data or "Information" in data:
            print(f"Alpha Vantage API error: {data.get('Error Message', data.get('Information'))}")
            return None
        
        # Parse time series data
        ts_key = "Time Series (60min)"
        if ts_key not in data:
            return None
        
        time_series = data[ts_key]
        latest_time = list(time_series.keys())[0]
        latest_data = time_series[latest_time]
        
        return {
            "timestamp": latest_time,
            "open": float(latest_data.get("1. open", 0)),
            "high": float(latest_data.get("2. high", 0)),
            "low": float(latest_data.get("3. low", 0)),
            "close": float(latest_data.get("4. close", 0)),
            "volume": int(latest_data.get("5. volume", 0))
        }
    
    except Exception as e:
        print(f"Alpha Vantage error: {e}")
        return None


def get_rsi(symbol: str, api_key: Optional[str] = None) -> Optional[float]:
    """
    Get RSI (Relative Strength Index) indicator.
    
    Args:
        symbol: Trading symbol
        api_key: Alpha Vantage API key
    
    Returns:
        RSI value (0-100) or None
    """
    key = initialize_alphavantage(api_key)
    
    try:
        params = {
            "function": "RSI",
            "symbol": symbol,
            "interval": "daily",
            "time_period": 14,
            "apikey": key
        }
        
        response = requests.get(ALPHAVANTAGE_BASE, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if "Technical Analysis: RSI" not in data:
            return None
        
        rsi_data = data["Technical Analysis: RSI"]
        latest_date = list(rsi_data.keys())[0]
        rsi_value = float(rsi_data[latest_date].get("RSI", 0))
        
        return rsi_value
    
    except Exception as e:
        print(f"Alpha Vantage RSI error: {e}")
        return None
