import os
from dotenv import load_dotenv

# Load .env file
load_dotenv('.env')

# Check keys
print('=== API KEY CHECK ===')
print(f'GEMINI_API_KEY: {"✅" if os.getenv("GEMINI_API_KEY") else "❌"}')
print(f'GROQ_KEY: {"✅" if os.getenv("GROQ_KEY") else "❌"}')
print(f'HUGGINGFACE_KEY: {"✅" if os.getenv("HUGGINGFACE_KEY") else "❌"}')
print(f'REPLICATE_KEY: {"✅" if os.getenv("REPLICATE_KEY") else "❌"}')
print(f'NEWSAPI_KEY: {"✅" if os.getenv("NEWSAPI_KEY") else "❌"}')
