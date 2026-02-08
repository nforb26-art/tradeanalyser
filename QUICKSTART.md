# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Windows

1. **Run the startup script:**
   ```bash
   start.bat
   ```
   
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Start the server on http://localhost:8000

2. **Open your browser:**
   ```
   http://localhost:8000
   ```

### Linux / Mac

1. **Run the startup script:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

2. **Open your browser:**
   ```
   http://localhost:8000
   ```

### Manual Setup (Advanced)

If you prefer manual setup:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and add your API keys

# 5. Run server
python backend/main.py
```

## 📝 Add Your API Keys

Before the AI analysis works, add your free API keys to `.env`:

1. **Google Gemini API** (for AI analysis)
   - Go to: https://makersuite.google.com/app/apikey
   - Click "Create API Key"
   - Copy to `.env`: `GEMINI_API_KEY=your_key`

2. **NewsAPI** (for sentiment analysis)
   - Go to: https://newsapi.org
   - Sign up and get your key
   - Copy to `.env`: `NEWSAPI_KEY=your_key`

3. **Alpha Vantage** (optional, for technical indicators)
   - Go to: https://www.alphavantage.co/api/
   - Get your key
   - Copy to `.env`: `ALPHAVANTAGE_KEY=your_key`

## 🔍 Try It Out

1. **Search for a crypto:**
   - Type "Bitcoin" or "BTC" in the search box
   - Click the result to analyze

2. **Or pick from trending:**
   - Click any trending pair card
   - Wait for analysis (5-8 seconds)

3. **Review the results:**
   - Entry, Stop Loss, Take Profit levels
   - AI sentiment and trading signal
   - News sentiment
   - Market data

## 💡 What Each Value Means

- **Entry Point**: Where to open your trade (current price)
- **Stop Loss**: Your exit if price goes down (risk limit)
- **Take Profit**: Your exit if price goes up (profit target)
- **Risk/Reward Ratio**: How much profit potential vs. risk
- **AI Signal**: Gemini AI recommendation (BUY/HOLD/SELL)
- **Confidence**: How confident the AI is (0-10 scale)

## ⚠️ Important Notes

- **Not Financial Advice**: This is for educational purposes only
- **Always DYOR**: Do your own research
- **Test First**: Paper trade before real money
- **API Limits**: Free tiers have rate limits (see README)

## 🆘 Troubleshooting

**"Cannot connect to localhost:8000"**
- Make sure the server is running
- Check if port 8000 is not in use: `netstat -ano | findstr :8000`
- Try `http://127.0.0.1:8000` instead

**"No API key configured"**
- Create `.env` file (copy from `.env.example`)
- Add your API keys
- Restart the server

**"Search returns no results"**
- CoinGecko might be rate-limited
- Wait a few seconds and try again
- Use exact cryptocurrency name

**"Analysis takes too long"**
- Normal first time (5-8 seconds)
- Gemini API can be slower
- Check your internet connection

## 📚 Learn More

- See `README.md` for full documentation
- Check API docs: https://docs.coingecko.com/reference/
- Gemini API: https://ai.google.dev/
- NewsAPI: https://newsapi.org/docs

---

**Enjoy! 🚀** Happy trading analysis!
