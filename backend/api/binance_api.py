"""Binance API client for cryptocurrency market data (free, no key required)."""

import requests
from typing import Dict, Optional


def get_ticker_data(symbol: str) -> Dict:
    """
    Get real-time ticker data from Binance.
    
    Args:
        symbol: Trading pair (e.g., 'BTCUSDT', 'ETHUSDT')
    
    Returns:
        Dictionary with ticker data and status
    """
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr"
        params = {"symbol": symbol}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "available": True,
                "symbol": data.get("symbol"),
                "price": float(data.get("lastPrice", 0)),
                "high_24h": float(data.get("highPrice", 0)),
                "low_24h": float(data.get("lowPrice", 0)),
                "volume_24h": float(data.get("volume", 0)),
                "change_24h": float(data.get("priceChangePercent", 0)),
                "bid": float(data.get("bidPrice", 0)),
                "ask": float(data.get("askPrice", 0))
            }
        elif response.status_code == 400:
            return {
                "available": False,
                "error": f"Trading pair '{symbol}' not found on Binance",
                "suggestion": "Check symbol format (e.g., BTCUSDT, ETHUSDT)"
            }
        else:
            return {
                "available": False,
                "error": f"Binance API error: {response.status_code}",
                "status": response.status_code
            }
    
    except requests.exceptions.Timeout:
        return {
            "available": False,
            "error": "Binance API request timed out (>10 seconds)",
            "suggestion": "Try again in a few seconds"
        }
    
    except requests.exceptions.ConnectionError:
        return {
            "available": False,
            "error": "Cannot connect to Binance API",
            "suggestion": "Check your internet connection"
        }
    
    except Exception as e:
        return {
            "available": False,
            "error": f"Binance API error: {str(e)}",
            "type": type(e).__name__
        }


def get_order_book_depth(symbol: str, limit: int = 5) -> Dict:
    """
    Get order book depth (bid/ask spread) from Binance.
    
    Args:
        symbol: Trading pair (e.g., 'BTCUSDT')
        limit: Number of orders to fetch (default 5)
    
    Returns:
        Dictionary with order book data
    """
    try:
        url = f"https://api.binance.com/api/v3/depth"
        params = {"symbol": symbol, "limit": limit}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "available": True,
                "bids": data.get("bids", []),
                "asks": data.get("asks", []),
                "spread_percentage": calculate_spread(data.get("bids"), data.get("asks"))
            }
        else:
            return {"available": False, "error": f"API error: {response.status_code}"}
    
    except Exception as e:
        return {"available": False, "error": str(e)}


def calculate_spread(bids: list, asks: list) -> float:
    """Calculate bid-ask spread percentage."""
    if not bids or not asks:
        return 0.0
    
    highest_bid = float(bids[0][0]) if bids else 0
    lowest_ask = float(asks[0][0]) if asks else 0
    
    if highest_bid == 0:
        return 0.0
    
    return ((lowest_ask - highest_bid) / highest_bid) * 100
