#!/usr/bin/env python3
"""Test script to verify BTC/USDT analysis with multiple AIs"""

import requests
import json
import time

API_URL = "http://127.0.0.1:8000/api/analyze"

# Test with BTC/USDT
test_data = {
    "crypto_id": "bitcoin",
    "symbol": "BTC/USDT"
}

print("=" * 80)
print("Testing Crypto Analyzer with BTC/USDT")
print("=" * 80)
print(f"Sending request: {test_data}")
print()

start_time = time.time()

try:
    response = requests.post(API_URL, json=test_data, timeout=30)
    elapsed = time.time() - start_time
    
    print(f"Response Time: {elapsed:.2f} seconds")
    print(f"Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Analysis successful!")
        print()
        
        # Display key results
        print(f"Pair: {data.get('pair', 'N/A')}")
        print(f"Current Price: ${data.get('current_price', 'N/A')}")
        print(f"24h Change: {data.get('change_24h', 'N/A')}%")
        print()
        
        # Sentiment Analysis
        sentiment = data.get('sentiment', {})
        print("SENTIMENT ANALYSIS:")
        print(f"  Consensus: {sentiment.get('consensus', 'N/A')}")
        print(f"  Confidence: {sentiment.get('confidence', 'N/A')}/10")
        print(f"  Available Models: {sentiment.get('available_models', 0)}")
        print()
        
        # Individual AI Models
        print("INDIVIDUAL AI MODELS:")
        models = sentiment.get('models', {})
        for model_name, model_data in models.items():
            available = model_data.get('available', False)
            status = "✓" if available else "✗"
            sentiment_val = model_data.get('sentiment', 'N/A')
            confidence = model_data.get('confidence', 'N/A')
            print(f"  {status} {model_name.upper():15} - {sentiment_val:6} (Confidence: {confidence})")
        print()
        
        # Trading Levels
        print("TRADING LEVELS:")
        print(f"  Entry:      ${data.get('entry', 'N/A')}")
        print(f"  Stop Loss:  ${data.get('stoploss', 'N/A')}")
        print(f"  Take Profit: ${data.get('takeprofit', 'N/A')}")
        print()
        
        # Risk/Reward
        print(f"Risk/Reward Ratio: {data.get('risk_reward_ratio', 'N/A')}")
        
        # Check if at least 2 models are available
        available_count = sum(1 for m in models.values() if m.get('available', False))
        print()
        print(f"✓ Total Available Models: {available_count}/3")
        if available_count >= 2:
            print("✓ CONSENSUS REQUIREMENT MET (2+ models available)")
        else:
            print("⚠ WARNING: Less than 2 models available!")
            
    else:
        print(f"✗ Error Response:")
        print(response.text)
        
except requests.Timeout:
    elapsed = time.time() - start_time
    print(f"✗ Request timeout after {elapsed:.2f} seconds")
except Exception as e:
    print(f"✗ Error: {str(e)}")

print()
print("=" * 80)
