"""Hugging Face API integration for free sentiment analysis using various models."""

import requests
import os
from typing import Optional, Dict

HUGGINGFACE_BASE = "https://api-inference.huggingface.co/models"


def initialize_huggingface(api_key: Optional[str] = None) -> str:
    """Get Hugging Face API key from parameter or environment."""
    return api_key or os.getenv("HUGGINGFACE_KEY", "")


def analyze_sentiment_huggingface(text: str, api_key: Optional[str] = None) -> Dict:
    """
    Analyze sentiment using Hugging Face distilbert model (fast).
    
    Args:
        text: Text to analyze
        api_key: Hugging Face API key
    
    Returns:
        Dictionary with sentiment score and label
    """
    key = initialize_huggingface(api_key)
    if not key:
        return {"error": "Hugging Face API key not configured", "available": False}
    
    try:
        # Use faster distilbert model for sentiment analysis
        url = f"{HUGGINGFACE_BASE}/distilbert-base-uncased-finetuned-sst-2-english"
        headers = {"Authorization": f"Bearer {key}"}
        
        payload = {"inputs": text}
        
        response = requests.post(url, json=payload, headers=headers, timeout=8)
        response.raise_for_status()
        
        result = response.json()
        
        # Check for error in response
        if "error" in result:
            return {"error": f"Hugging Face error: {result.get('error', 'Unknown')}", "available": False}
        
        # Extract sentiment from result
        if result and len(result) > 0:
            scores = result[0]
            if isinstance(scores, list) and len(scores) > 0:
                # Get top classification
                best = max(scores, key=lambda x: x['score'])
                label = best['label'].upper()
                score = best['score']
                
                # Map to trading sentiment
                if 'POSITIVE' in label or label == 'GOOD':
                    sentiment = "BULLISH"
                elif 'NEGATIVE' in label or label == 'BAD':
                    sentiment = "BEARISH"
                else:
                    sentiment = "NEUTRAL"
                
                return {
                    "sentiment": sentiment,
                    "confidence": round(score * 10, 1),  # Scale to 0-10
                    "available": True
                }
        
        return {"sentiment": "NEUTRAL", "confidence": 5, "available": True}
    
    except requests.exceptions.Timeout:
        return {"error": "Hugging Face timeout", "available": False}
    except Exception as e:
        return {"error": f"Hugging Face error: {str(e)}", "available": False}


def predict_market_trend(historical_data: str, api_key: Optional[str] = None) -> Dict:
    """
    Use Hugging Face text generation for market trend analysis.
    
    Args:
        historical_data: Market data description
        api_key: Hugging Face API key
    
    Returns:
        Dictionary with trend prediction
    """
    key = initialize_huggingface(api_key)
    if not key:
        return {"error": "Hugging Face API key not configured"}
    
    try:
        # Use text generation model
        url = f"{HUGGINGFACE_BASE}/gpt2"
        headers = {"Authorization": f"Bearer {key}"}
        
        payload = {
            "inputs": f"Based on market data: {historical_data}. Market trend prediction:",
            "parameters": {"max_length": 100}
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        
        if "error" in result:
            return {"error": f"Hugging Face error: {result['error']}"}
        
        if isinstance(result, list) and len(result) > 0:
            return {
                "prediction": result[0].get("generated_text", ""),
                "available": True
            }
        
        return {"error": "No prediction generated"}
    
    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}
