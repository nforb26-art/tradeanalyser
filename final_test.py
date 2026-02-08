#!/usr/bin/env python3
"""Final comprehensive test of BTC/USDT analysis"""

import requests
import time
import sys

def test_analyze():
    url = 'http://127.0.0.1:8000/api/analyze'
    payload = {
        'crypto_id': 'bitcoin',
        'symbol': 'BTC/USDT'
    }
    
    print("=" * 80)
    print("CRYPTO ANALYZER - BTC/USDT TEST")
    print("=" * 80)
    print()
    print(f"Endpoint: {url}")
    print(f"Payload: {payload}")
    print()
    print("Sending request...")
    
    start = time.time()
    
    try:
        response = requests.post(url, json=payload, timeout=35)
        elapsed = time.time() - start
        
        print(f"Response received in {elapsed:.2f} seconds")
        print(f"Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            
            print("✓ ANALYSIS SUCCESSFUL!")
            print()
            print("=" * 80)
            print("TRADING PAIR DETAILS")
            print("=" * 80)
            print(f"Pair:            {data.get('pair')}")
            print(f"Current Price:   ${data.get('current_price')}")
            print(f"24h Change:      {data.get('change_24h')}%")
            print(f"Volatility:      {data.get('volatility')} ({data.get('volatility_percent')}%)")
            print()
            
            print("=" * 80)
            print("TRADING LEVELS")
            print("=" * 80)
            print(f"Entry Point:     ${data.get('entry')}")
            print(f"Stop Loss:       ${data.get('stoploss')}")
            print(f"Take Profit:     ${data.get('takeprofit')}")
            print(f"SL% / TP%:       {data.get('sl_percentage')}% / {data.get('tp_percentage')}%")
            print(f"Risk/Reward:     {data.get('risk_reward_ratio')}")
            print()
            
            sentiment = data.get('sentiment', {})
            models = sentiment.get('models', {})
            
            print("=" * 80)
            print("AI CONSENSUS")
            print("=" * 80)
            print(f"Consensus Signal: {sentiment.get('consensus')}")
            print(f"Confidence:       {sentiment.get('confidence')}/10")
            print(f"Available Models: {sentiment.get('available_models')}/3")
            print()
            
            print("=" * 80)
            print("INDIVIDUAL AI MODELS")
            print("=" * 80)
            
            model_count = 0
            for name, model_data in models.items():
                available = model_data.get('available', False)
                if available:
                    model_count += 1
                    
                status = "✓ ACTIVE" if available else "✗ UNAVAILABLE"
                sentiment_val = model_data.get('sentiment', 'N/A')
                confidence = model_data.get('confidence', 'N/A')
                
                print(f"{status:20} {name.upper():12} - Signal: {sentiment_val:8} Confidence: {confidence}")
            
            print()
            print("=" * 80)
            print("TEST RESULTS")
            print("=" * 80)
            print(f"Total Time:      {elapsed:.2f} seconds")
            print(f"Working Models:  {model_count}/3")
            
            if model_count >= 2:
                print("✓ CONSENSUS REQUIREMENT MET (2+ models confirmed)")
            else:
                print("⚠ WARNING: Only 1 model working (need 2+)")
            
            if elapsed < 12:
                print("✓ SPEED EXCELLENT (< 12 seconds)")
            elif elapsed < 20:
                print("✓ SPEED GOOD (< 20 seconds)")
            else:
                print("⚠ SPEED SLOW (> 20 seconds)")
        
        else:
            print(f"✗ ERROR Response ({response.status_code}):")
            print(response.text)
            
    except requests.Timeout:
        elapsed = time.time() - start
        print(f"✗ TIMEOUT after {elapsed:.2f} seconds")
    except requests.ConnectionError:
        print("✗ CONNECTION ERROR - Server not running?")
    except Exception as e:
        print(f"✗ ERROR: {e}")

if __name__ == '__main__':
    test_analyze()
