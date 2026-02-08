"""NewsAPI integration for market sentiment (free tier available)."""

import requests
import os
from typing import List, Dict, Optional

NEWSAPI_BASE = "https://newsapi.org/v2"


def initialize_newsapi(api_key: Optional[str] = None) -> str:
    """Get NewsAPI key from parameter or environment."""
    return api_key or os.getenv("NEWSAPI_KEY", "")


def get_crypto_news(crypto_name: str, api_key: Optional[str] = None) -> List[Dict]:
    """
    Get recent news articles about a cryptocurrency.
    
    Args:
        crypto_name: Cryptocurrency name (e.g., "Bitcoin")
        api_key: NewsAPI key
    
    Returns:
        List of news articles
    """
    key = initialize_newsapi(api_key)
    if not key:
        print("NewsAPI key not configured")
        return []
    
    try:
        url = f"{NEWSAPI_BASE}/everything"
        params = {
            "q": f'"{crypto_name}" cryptocurrency',
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": key,
            "pageSize": 5
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "published_at": article.get("publishedAt", ""),
                "source": article.get("source", {}).get("name", "")
            })
        
        return articles
    
    except Exception as e:
        print(f"NewsAPI error: {e}")
        return []


def calculate_sentiment_from_news(articles: List[Dict]) -> float:
    """
    Simple sentiment calculation from article titles (mock implementation).
    
    Args:
        articles: List of news articles
    
    Returns:
        Sentiment score from -1 (bearish) to 1 (bullish)
    """
    if not articles:
        return 0.0
    
    bullish_keywords = ["surge", "rally", "gain", "pump", "bull", "recovery", "moon"]
    bearish_keywords = ["crash", "drop", "fall", "dump", "bear", "loss", "burn"]
    
    score = 0.0
    for article in articles:
        title = article.get("title", "").lower()
        for keyword in bullish_keywords:
            if keyword in title:
                score += 0.1
        for keyword in bearish_keywords:
            if keyword in title:
                score -= 0.1
    
    # Normalize to -1 to 1
    return max(-1.0, min(1.0, score))
