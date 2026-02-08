"""CryptoPanic API for crypto-specific news (free, no key required)."""

import requests
from typing import Dict, List


def get_crypto_news(crypto_id: str = "", limit: int = 5) -> Dict:
    """
    Get latest crypto news from CryptoPanic.
    
    Args:
        crypto_id: Cryptocurrency ID (e.g., 'bitcoin', 'ethereum')
        limit: Number of news items to fetch (default 5)
    
    Returns:
        Dictionary with news items and sentiment
    """
    try:
        url = "https://cryptopanic.com/api/v1/posts/"
        params = {
            "auth_token": "874ea776f07fbf76ad84ee3f7bfa9d67de7dc92f",  # Public demo token
            "kind": "news",
            "limit": limit,
            "sort": "created_at",
            "order": "descending"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            news_items = []
            sentiment_sum = 0
            
            for item in results[:limit]:
                title = item.get("title", "")
                source = item.get("source", {}).get("title", "Unknown")
                url_item = item.get("url", "")
                published = item.get("published_at", "")
                
                # CryptoPanic provides vote_negative and vote_positive
                positive = item.get("vote_positive", 0)
                negative = item.get("vote_negative", 0)
                
                # Calculate sentiment
                total_votes = positive + negative
                if total_votes > 0:
                    sentiment_score = (positive - negative) / total_votes
                else:
                    sentiment_score = 0
                
                sentiment_sum += sentiment_score
                
                news_items.append({
                    "title": title,
                    "source": source,
                    "url": url_item,
                    "published": published,
                    "positive_votes": positive,
                    "negative_votes": negative,
                    "sentiment": sentiment_score
                })
            
            # Calculate average sentiment
            avg_sentiment = sentiment_sum / len(news_items) if news_items else 0
            
            # Convert to label
            if avg_sentiment > 0.2:
                sentiment_label = "POSITIVE"
            elif avg_sentiment < -0.2:
                sentiment_label = "NEGATIVE"
            else:
                sentiment_label = "NEUTRAL"
            
            return {
                "available": True,
                "source": "CryptoPanic",
                "news_count": len(news_items),
                "news": news_items,
                "average_sentiment": avg_sentiment,
                "sentiment": sentiment_label,
                "confidence": min(10, max(1, int(5 + avg_sentiment * 5)))
            }
        
        elif response.status_code == 429:
            return {
                "available": False,
                "error": "CryptoPanic rate limit hit",
                "suggestion": "Try again in a few seconds"
            }
        
        else:
            return {
                "available": False,
                "error": f"CryptoPanic API error: {response.status_code}",
                "status": response.status_code
            }
    
    except requests.exceptions.Timeout:
        return {
            "available": False,
            "error": "CryptoPanic request timed out",
            "suggestion": "Try again in a few seconds"
        }
    
    except requests.exceptions.ConnectionError:
        return {
            "available": False,
            "error": "Cannot connect to CryptoPanic",
            "suggestion": "Check your internet connection"
        }
    
    except Exception as e:
        return {
            "available": False,
            "error": f"CryptoPanic error: {str(e)}",
            "type": type(e).__name__
        }


def get_trending_news(limit: int = 3) -> Dict:
    """Get trending crypto news."""
    try:
        url = "https://cryptopanic.com/api/v1/posts/"
        params = {
            "auth_token": "874ea776f07fbf76ad84ee3f7bfa9d67de7dc92f",
            "kind": "news",
            "limit": limit,
            "sort": "votes",
            "order": "descending"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            trending = []
            for item in results[:limit]:
                trending.append({
                    "title": item.get("title", ""),
                    "source": item.get("source", {}).get("title", ""),
                    "votes": item.get("vote_positive", 0) + item.get("vote_negative", 0)
                })
            
            return {"available": True, "trending": trending}
        
        else:
            return {"available": False, "error": f"API error: {response.status_code}"}
    
    except Exception as e:
        return {"available": False, "error": str(e)}
