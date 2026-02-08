"""RSS Feed parser for crypto news from multiple free sources."""

import requests
import xml.etree.ElementTree as ET
from typing import Dict, List
from datetime import datetime


def get_coindesk_news(limit: int = 5) -> Dict:
    """
    Get news from CoinDesk RSS feed (free).
    
    Args:
        limit: Number of articles to fetch
    
    Returns:
        Dictionary with news items
    """
    try:
        url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            articles = []
            items = root.findall(".//item")
            
            for item in items[:limit]:
                title_elem = item.find("title")
                link_elem = item.find("link")
                desc_elem = item.find("description")
                pub_elem = item.find("pubDate")
                
                articles.append({
                    "title": title_elem.text if title_elem is not None else "N/A",
                    "link": link_elem.text if link_elem is not None else "N/A",
                    "description": desc_elem.text if desc_elem is not None else "",
                    "published": pub_elem.text if pub_elem is not None else "N/A",
                    "source": "CoinDesk"
                })
            
            return {
                "available": True,
                "source": "CoinDesk",
                "articles": articles,
                "count": len(articles)
            }
        
        else:
            return {
                "available": False,
                "error": f"CoinDesk RSS error: {response.status_code}",
                "source": "CoinDesk"
            }
    
    except requests.exceptions.Timeout:
        return {
            "available": False,
            "error": "CoinDesk request timed out",
            "source": "CoinDesk"
        }
    
    except Exception as e:
        return {
            "available": False,
            "error": f"CoinDesk error: {str(e)}",
            "source": "CoinDesk",
            "type": type(e).__name__
        }


def get_cointelegraph_news(limit: int = 5) -> Dict:
    """
    Get news from Cointelegraph RSS feed (free).
    
    Args:
        limit: Number of articles to fetch
    
    Returns:
        Dictionary with news items
    """
    try:
        url = "https://cointelegraph.com/feed"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            articles = []
            items = root.findall(".//item")
            
            for item in items[:limit]:
                title_elem = item.find("title")
                link_elem = item.find("link")
                desc_elem = item.find("description")
                pub_elem = item.find("pubDate")
                
                articles.append({
                    "title": title_elem.text if title_elem is not None else "N/A",
                    "link": link_elem.text if link_elem is not None else "N/A",
                    "description": desc_elem.text if desc_elem is not None else "",
                    "published": pub_elem.text if pub_elem is not None else "N/A",
                    "source": "Cointelegraph"
                })
            
            return {
                "available": True,
                "source": "Cointelegraph",
                "articles": articles,
                "count": len(articles)
            }
        
        else:
            return {
                "available": False,
                "error": f"Cointelegraph RSS error: {response.status_code}",
                "source": "Cointelegraph"
            }
    
    except requests.exceptions.Timeout:
        return {
            "available": False,
            "error": "Cointelegraph request timed out",
            "source": "Cointelegraph"
        }
    
    except Exception as e:
        return {
            "available": False,
            "error": f"Cointelegraph error: {str(e)}",
            "source": "Cointelegraph",
            "type": type(e).__name__
        }


def get_messari_news(limit: int = 5) -> Dict:
    """
    Get news from Messari RSS feed (free).
    
    Args:
        limit: Number of articles to fetch
    
    Returns:
        Dictionary with news items
    """
    try:
        url = "https://messari.io/api/v1/news?limit=" + str(limit)
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = []
            
            for item in data.get("data", [])[:limit]:
                articles.append({
                    "title": item.get("title", "N/A"),
                    "link": item.get("content_url", "N/A"),
                    "description": item.get("description", ""),
                    "published": item.get("published_at", "N/A"),
                    "source": "Messari"
                })
            
            return {
                "available": True,
                "source": "Messari",
                "articles": articles,
                "count": len(articles)
            }
        
        elif response.status_code == 429:
            return {
                "available": False,
                "error": "Messari rate limited",
                "source": "Messari"
            }
        
        else:
            return {
                "available": False,
                "error": f"Messari API error: {response.status_code}",
                "source": "Messari"
            }
    
    except requests.exceptions.Timeout:
        return {
            "available": False,
            "error": "Messari request timed out",
            "source": "Messari"
        }
    
    except Exception as e:
        return {
            "available": False,
            "error": f"Messari error: {str(e)}",
            "source": "Messari",
            "type": type(e).__name__
        }


def get_all_rss_news(limit: int = 3) -> Dict:
    """
    Get news from all RSS sources.
    
    Args:
        limit: Number of articles per source
    
    Returns:
        Dictionary with all news sources
    """
    return {
        "coindesk": get_coindesk_news(limit),
        "cointelegraph": get_cointelegraph_news(limit),
        "messari": get_messari_news(limit)
    }
