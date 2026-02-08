#!/usr/bin/env python3
"""Quick performance test"""
import requests
import time

start = time.time()
r = requests.post('http://127.0.0.1:8000/api/analyze', 
                 json={'crypto_id': 'bitcoin', 'symbol': 'BTC/USDT'}, 
                 timeout=15)
elapsed = time.time() - start

print(f'Total Time: {elapsed:.2f}s')
print(f'Status: {r.status_code}')

if r.status_code == 200:
    d = r.json()
    print(f"\n✓ Success!")
    print(f"Pair: {d.get('pair')}")
    
    models = d.get('sentiment', {}).get('models', {})
    available = sum(1 for m in models.values() if m.get('available'))
    print(f"Working Models: {available}/3")
    
    for name, m in models.items():
        status = '✓' if m.get('available') else '✗'
        print(f"  {status} {name}: {m.get('sentiment', 'N/A')}")
else:
    print(f"✗ Error: {r.text[:100]}")
