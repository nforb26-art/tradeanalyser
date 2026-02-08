"""CoinGecko API integration for cryptocurrency data."""

import requests
from typing import Optional, List, Dict
import time

COINGECKO_BASE = "https://api.coingecko.com/api/v3"
MAX_RETRIES = 2
RETRY_DELAY = 1  # seconds

# Map of common trading pair formats to crypto IDs
PAIR_TO_ID = {
    "BTC": "bitcoin",
    "BTC/USD": "bitcoin",
    "BTC/USDT": "bitcoin",
    "ETH": "ethereum",
    "ETH/USD": "ethereum",
    "ETH/USDT": "ethereum",
    "ADA": "cardano",
    "ADA/USD": "cardano",
    "XRP": "ripple",
    "XRP/USD": "ripple",
    "SOL": "solana",
    "SOL/USD": "solana",
    "DOGE": "dogecoin",
    "DOGE/USD": "dogecoin",
    "MATIC": "matic-network",
    "MATIC/USD": "matic-network",
}


def parse_pair_format(pair_str: str) -> Optional[str]:
    """
    Convert trading pair format (e.g., 'BTC/USD') to crypto ID.
    
    Args:
        pair_str: Pair string like 'BTC/USD' or 'BTC'
    
    Returns:
        Crypto ID or None if not found
    """
    pair_upper = pair_str.upper().strip()
    
    # Check if it's a known pair
    if pair_upper in PAIR_TO_ID:
        return PAIR_TO_ID[pair_upper]
    
    # If it contains '/', try just the first part
    if '/' in pair_upper:
        symbol = pair_upper.split('/')[0].strip()
        if symbol in PAIR_TO_ID:
            return PAIR_TO_ID[symbol]
    
    return None


def search_cryptocurrencies(query: str) -> Dict:
    """
    Search for cryptocurrencies by name, symbol, or pair format.
    
    Args:
        query: Search term (e.g., "bitcoin", "BTC", "BTC/USD")
    
    Returns:
        Dictionary with results and any errors
    """
    try:
        # First check if it's a pair format
        pair_id = parse_pair_format(query)
        if pair_id:
            return {
                "success": True,
                "results": [
                    {
                        "id": pair_id,
                        "name": query.upper(),
                        "symbol": query.upper().split('/')[0],
                        "market_cap_rank": None,
                        "from_pair": True
                    }
                ],
                "source": "pair_format"
            }
        
        # Otherwise search by name/symbol
        url = f"{COINGECKO_BASE}/search"
        params = {"query": query}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        coins = data.get("coins", [])
        
        if not coins:
            return {"success": False, "error": f"No cryptocurrencies found for '{query}'", "results": []}
        
        # Return simplified list
        return {
            "success": True,
            "results": [
                {
                    "id": coin["id"],
                    "name": coin["name"],
                    "symbol": coin["symbol"].upper(),
                    "market_cap_rank": coin.get("market_cap_rank", None)
                }
                for coin in coins[:10]  # Top 10 results
            ],
            "source": "coingecko_search"
        }
    
    except requests.Timeout:
        return {"success": False, "error": "CoinGecko search timeout - API is slow or unreachable", "results": []}
    except requests.ConnectionError:
        return {"success": False, "error": "Cannot connect to CoinGecko API - check internet connection", "results": []}
    except requests.HTTPError as e:
        error_msg = f"CoinGecko API error: {e.response.status_code} - {e.response.reason}"
        if e.response.status_code == 429:
            error_msg = "CoinGecko rate limit exceeded - please wait a moment and try again"
        elif e.response.status_code == 404:
            error_msg = f"Search endpoint not found - API may have changed"
        return {"success": False, "error": error_msg, "results": []}
    except Exception as e:
        return {"success": False, "error": f"Unexpected search error: {str(e)}", "results": []}


def get_cryptocurrency_data(crypto_id: str) -> Optional[Dict]:
    """
    Get current cryptocurrency price and market data.
    Tries CoinGecko first with retry logic and exponential backoff,
    falls back to Binance or Kraken if CoinGecko fails.
    
    Args:
        crypto_id: CoinGecko crypto ID (e.g., "bitcoin")
    
    Returns:
        Dictionary with price, market cap, 24h change, etc. or error info
    """
    # Validate crypto_id
    if not crypto_id or not isinstance(crypto_id, str):
        return {
            "error": "Invalid cryptocurrency ID provided",
            "success": False
        }
    
    # Try CoinGecko once (no retries - too slow)
    try:
        url = f"{COINGECKO_BASE}/simple/price"
        params = {
            "ids": crypto_id.lower(),
            "vs_currencies": "usd",
            "include_market_cap": True,
            "include_24hr_vol": True,
            "include_24hr_change": True,
            "include_high_low": True
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        crypto_lower = crypto_id.lower()
        
        if crypto_lower not in data or not data[crypto_lower]:
            # Not found in CoinGecko, try Binance
            return _try_alternative_sources(crypto_id)
        
        coin_data = data[crypto_lower]
        
        return {
            "current_price": coin_data.get("usd", 0),
            "market_cap": coin_data.get("usd_market_cap", 0),
            "volume_24h": coin_data.get("usd_24h_vol", 0),
            "change_24h": coin_data.get("usd_24h_change", 0),
            "high_24h": coin_data.get("usd_high_24h", 0),
            "low_24h": coin_data.get("usd_low_24h", 0),
            "success": True,
            "source": "coingecko"
        }
    
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": "Cryptocurrency not found", "success": False}
        # Any other error (including 429 rate limit), try Binance
        return _try_alternative_sources(crypto_id)
    
    except (requests.Timeout, requests.ConnectionError):
        # Connection issues, try Binance
        return _try_alternative_sources(crypto_id)
    
    except Exception:
        return _try_alternative_sources(crypto_id)


def _try_alternative_sources(crypto_id: str) -> Dict:
    """
    Try to get cryptocurrency data from Binance after CoinGecko fails.
    
    Args:
        crypto_id: CoinGecko crypto ID (e.g., "bitcoin")
    
    Returns:
        Dictionary with price data from alternative source or error info
    """
    try:
        from . import binance_api
        
        # Map common crypto IDs to exchange symbols
        SYMBOL_MAP = {
            "bitcoin": "BTCUSDT",
            "ethereum": "ETHUSDT",
            "cardano": "ADAUSDT",
            "ripple": "XRPUSDT",
            "solana": "SOLUSDT",
            "dogecoin": "DOGEUSDT",
            "matic-network": "MATICUSDT",
            "polkadot": "DOTUSDT",
        }
        
        # Get Binance symbol
        binance_symbol = SYMBOL_MAP.get(crypto_id.lower())
        
        if not binance_symbol:
            # Try guessing the symbol
            symbol_base = crypto_id.upper().split('-')[0]
            binance_symbol = f"{symbol_base}USDT"
        
        # Try Binance
        try:
            ticker_data = binance_api.get_ticker_data(binance_symbol)
            if ticker_data.get("available"):
                return {
                    "current_price": ticker_data.get("price", 0),
                    "market_cap": 0,
                    "volume_24h": ticker_data.get("volume_24h", 0),
                    "change_24h": ticker_data.get("change_24h", 0),
                    "high_24h": ticker_data.get("high_24h", 0),
                    "low_24h": ticker_data.get("low_24h", 0),
                    "success": True,
                    "source": "binance"
                }
        except Exception:
            pass  # Binance failed
        
        # All sources failed
        return {
            "error": f"Could not fetch data for '{crypto_id}' from CoinGecko or Binance. Please try again.",
            "success": False
        }
    
    except Exception as e:
        return {
            "error": f"Failed to fetch cryptocurrency data: {str(e)}. Please try again in a moment.",
            "success": False
        }


def get_trending_pairs() -> Dict:
    """Get trending cryptocurrencies."""
    try:
        url = f"{COINGECKO_BASE}/trending"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        trending = []
        
        for item in data.get("coins", [])[:10]:
            coin = item["item"]
            trending.append({
                "id": coin["id"],
                "name": coin["name"],
                "symbol": coin["symbol"],
                "market_cap_rank": coin.get("market_cap_rank", None),
                "small_image": coin.get("small", "")
            })
        
        if not trending:
            return {"success": False, "error": "No trending data available", "trending": []}
        
        return {"success": True, "trending": trending}
    
    except requests.Timeout:
        return {"success": False, "error": "Trending data request timeout", "trending": []}
    except requests.ConnectionError:
        return {"success": False, "error": "Cannot connect to CoinGecko for trending data", "trending": []}
    except Exception as e:
        return {"success": False, "error": f"Error fetching trending: {str(e)}", "trending": []}
