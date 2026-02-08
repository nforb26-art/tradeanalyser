"""Kraken API client for cryptocurrency market data (free, no key required)."""

import requests
from typing import Dict


def get_ticker_data(pair: str) -> Dict:
    """
    Get real-time ticker data from Kraken.
    
    Args:
        pair: Trading pair (e.g., 'XBTUSDT', 'ETHUSDT', or standard names)
    
    Returns:
        Dictionary with ticker data and status
    """
    try:
        url = "https://api.kraken.com/0/public/Ticker"
        params = {"pair": pair}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for errors in response
            if data.get("error"):
                return {
                    "available": False,
                    "error": f"Kraken pair error: {data['error'][0]}",
                    "suggestion": f"Try formats like XBTUSDT or {pair.upper()}USD"
                }
            
            result = data.get("result", {})
            if not result:
                return {
                    "available": False,
                    "error": "Kraken returned empty result",
                    "suggestion": "Check pair name and try again"
                }
            
            pair_data = list(result.values())[0]
            
            return {
                "available": True,
                "pair": pair,
                "price": float(pair_data["c"][0]),  # last trade close price
                "high_24h": float(pair_data["h"][1]),  # 24h high
                "low_24h": float(pair_data["l"][1]),  # 24h low
                "volume_24h": float(pair_data["v"][1]),  # 24h volume
                "vwap": float(pair_data["p"][1]),  # volume weighted average price
                "trades": pair_data["t"][1]  # number of trades
            }
        
        else:
            return {
                "available": False,
                "error": f"Kraken API error: {response.status_code}",
                "status": response.status_code
            }
    
    except requests.exceptions.Timeout:
        return {
            "available": False,
            "error": "Kraken API request timed out (>10 seconds)",
            "suggestion": "Try again in a few seconds"
        }
    
    except requests.exceptions.ConnectionError:
        return {
            "available": False,
            "error": "Cannot connect to Kraken API",
            "suggestion": "Check your internet connection"
        }
    
    except (KeyError, IndexError) as e:
        return {
            "available": False,
            "error": f"Unexpected response format from Kraken: {str(e)}",
            "suggestion": "Check pair name (e.g., XBTUSDT for Bitcoin)"
        }
    
    except Exception as e:
        return {
            "available": False,
            "error": f"Kraken API error: {str(e)}",
            "type": type(e).__name__
        }


def get_spread(pair: str) -> Dict:
    """
    Get bid-ask spread from Kraken.
    
    Args:
        pair: Trading pair (e.g., 'XBTUSDT')
    
    Returns:
        Dictionary with spread information
    """
    try:
        url = "https://api.kraken.com/0/public/Ticker"
        params = {"pair": pair}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("error"):
                return {"available": False, "error": data["error"][0]}
            
            result = data.get("result", {})
            pair_data = list(result.values())[0]
            
            bid = float(pair_data["b"][0])
            ask = float(pair_data["a"][0])
            spread = ((ask - bid) / bid) * 100
            
            return {
                "available": True,
                "bid": bid,
                "ask": ask,
                "spread_percentage": spread
            }
        
        else:
            return {"available": False, "error": f"API error: {response.status_code}"}
    
    except Exception as e:
        return {"available": False, "error": str(e)}
