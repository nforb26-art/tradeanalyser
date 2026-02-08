import requests
import json
import time

print("Testing API analysis endpoint...")
print("=" * 50)

start = time.time()

# Test the analyze endpoint
response = requests.post(
    'http://localhost:8000/api/analyze', 
    json={'crypto_query': 'BTC'}, 
    timeout=60
)

elapsed = time.time() - start

print(f"Status: {response.status_code}")
print(f"Time taken: {elapsed:.1f} seconds")

if response.status_code == 200:
    data = response.json()
    print("\n✅ Response received!")
    print(f"Pair: {data.get('pair')}")
    print(f"Price: {data.get('current_price')}")
    print(f"Entry: {data.get('entry')}")
    print(f"Sentiment: {data.get('sentiment', {}).get('consensus')}")
    print(f"AI Models available: {data.get('sentiment', {}).get('available_models')}")
else:
    print(f"\n❌ Error: {response.text[:500]}")
