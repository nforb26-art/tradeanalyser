# Trade Analyzer - AI-Powered Cryptocurrency Trading Analysis

A full-stack web application that analyzes cryptocurrency trading pairs using multiple APIs and AI to provide entry points, stop losses, and take profit levels with precise decimal formatting.

## Features

- 🔍 **Real-time Cryptocurrency Search** - Search by name or symbol using CoinGecko
- 📊 **Multi-API Analysis** - Combines data from:
  - **CoinGecko** - Price and market data
  - **Google Gemini AI** - AI-powered market sentiment and trading signals
  - **NewsAPI** - Crypto news sentiment analysis
  - **Alpha Vantage** - Technical indicators (RSI, price data)
  
- 📈 **Trading Levels** - Automatically calculated:
  - Entry Point (current price)
  - Stop Loss (dynamic based on market conditions)
  - Take Profit (adjusted by sentiment)
  
- 🎯 **Precise Formatting**:
  - 4 decimal places for standard values
  - 8 decimal places for micro-cap cryptocurrencies
  - Risk/Reward ratio calculation
  
- 🔥 **Trending Pairs** - Explore trending cryptocurrencies
- 📱 **Responsive Design** - Works on desktop and mobile
- ⚡ **Real-time Sentiment Analysis** - AI-driven trading signals

## Tech Stack

**Backend:**
- Python 3.8+
- FastAPI
- Uvicorn
- Requests (HTTP client)
- google-generativeai (Gemini API)

**Frontend:**
- HTML5
- CSS3 (Dark theme)
- Vanilla JavaScript (ES6+)

**APIs:**
- CoinGecko API (free, no key required)
- Google Generative AI (Gemini)
- NewsAPI
- Alpha Vantage

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- API keys (see Configuration section)

### Setup Steps

1. **Clone or extract the repository:**
   ```bash
   cd "c:\Users\estate boss\Documents\trade analyser"
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys:**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your API keys (see Configuration section)

5. **Run the backend server:**
   ```bash
   python backend/main.py
   ```
   
   The server will start at `http://localhost:8000`

6. **Access the frontend:**
   Open your browser and go to `http://localhost:8000`

## Configuration

### API Keys

Get free API keys from these platforms:

#### 1. Google Gemini API (Required for AI analysis)
- Visit: https://makersuite.google.com/app/apikey
- Create a new API key
- Add to `.env`: `GEMINI_API_KEY=your_key_here`

#### 2. NewsAPI (Free tier available)
- Visit: https://newsapi.org
- Sign up and get your API key
- Add to `.env`: `NEWSAPI_KEY=your_key_here`

#### 3. Alpha Vantage (Free tier: 5 calls/min)
- Visit: https://www.alphavantage.co/api/
- Get your API key
- Add to `.env`: `ALPHAVANTAGE_KEY=your_key_here`

#### 4. CoinGecko API
- Free and public! No API key required.

### Environment Variables

Create `.env` file with:
```
GEMINI_API_KEY=your_gemini_key
NEWSAPI_KEY=your_newsapi_key
ALPHAVANTAGE_KEY=your_alphavantage_key
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

## Usage

### Web Interface

1. **Search for a cryptocurrency:**
   - Type in the search box (e.g., "Bitcoin", "BTC")
   - Click a result to analyze

2. **View Trending Pairs:**
   - Browse trending cryptocurrencies in the "Trending Now" section
   - Click any pair card to analyze

3. **Analyze Results:**
   - **Entry Point** - Recommended entry price
   - **Stop Loss** - Risk management level
   - **Take Profit** - Target exit level
   - **Risk/Reward Ratio** - Position sizing metric
   - **AI Sentiment** - Gemini AI analysis and signal (BUY/HOLD/SELL)
   - **News Sentiment** - Market sentiment from recent news
   - **Market Data** - Market cap, volume, 24h high/low

### API Endpoints

#### Search Cryptocurrencies
```bash
GET /api/search/{query}
# Example: /api/search/bitcoin
```

#### Get Trending Pairs
```bash
GET /api/trending
```

#### Analyze a Pair
```bash
POST /api/analyze
Content-Type: application/json

{
  "crypto_id": "bitcoin",
  "symbol": "BTC"
}
```

#### Health Check
```bash
GET /api/health
```

## Testing

Run the test suite:

```bash
pytest test_utils.py -v
```

Tests cover:
- Price formatting (standard and micro-cap)
- Analysis calculations
- Sentiment adjustments
- Risk/reward ratios

## Project Structure

```
trade analyser/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   ├── coingecko.py     # CoinGecko API client
│   │   ├── gemini_analysis.py # Gemini AI integration
│   │   ├── newsapi.py       # NewsAPI integration
│   │   └── alphavantage.py  # Alpha Vantage integration
│   └── utils/
│       ├── formatter.py     # Price formatting (4 decimals, etc)
│       └── analysis.py      # Trading analysis logic
├── frontend/
│   ├── index.html           # Main UI
│   ├── style.css            # Styling (dark theme)
│   └── app.js               # JavaScript logic
├── test_utils.py            # Unit tests
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
└── README.md                # This file
```

## Key Features Explained

### Decimal Formatting
- **Standard prices (USD, EUR)**: 4 decimal places (0.0001)
- **Micro-cap cryptocurrencies** (< 0.0001): Up to 8 decimal places as needed
- **Percentages**: 4 decimal places

Example:
- Bitcoin: 45,234.5678 USD
- Shib token: 0.00001234 USD

### Analysis Logic

1. **Entry Point**: Current market price
2. **Stop Loss**: 2% below entry (conservative risk management)
3. **Take Profit**: 
   - 5% above entry (neutral market)
   - 8% above entry (bullish sentiment)
   - 3% above entry (bearish sentiment)

4. **Risk/Reward Ratio**: Calculated as `(TP - Entry) / (Entry - SL)`

### AI Sentiment Scoring

Gemini AI analyzes:
- Current price and trends
- 24h price change
- Market cap and volume
- Provides: BUY, HOLD, or SELL signal with confidence score

NewsAPI analyzes:
- Recent news articles about the cryptocurrency
- Keyword-based sentiment: Bullish (positive keywords), Bearish (negative keywords)

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.8+)
- Verify all dependencies: `pip list`
- Reinstall dependencies: `pip install --upgrade -r requirements.txt`

### API Key errors
- Ensure `.env` file is in the root directory
- Check that all required keys are set
- Verify key validity on respective platforms

### CORS errors (frontend can't reach backend)
- Ensure backend is running on `http://localhost:8000`
- Check firewall settings
- Try accessing `http://localhost:8000/api/health` directly

### No results in search
- CoinGecko API may be rate-limited; try again in a few seconds
- Ensure internet connection is active
- Try exact cryptocurrency name (e.g., "Bitcoin" not "btc")

## Performance Notes

- CoinGecko requests: ~300ms
- Gemini AI analysis: ~2-5 seconds (first request slower)
- NewsAPI requests: ~1-2 seconds
- Total analysis time: ~5-8 seconds

## Rate Limits

- **CoinGecko**: ~10-50 calls/min (free tier)
- **Gemini**: 15 calls/min (free tier)
- **NewsAPI**: 100 calls/day (free tier)
- **Alpha Vantage**: 5 calls/min (free tier)

## Future Enhancements

- [ ] Historical price charts with TradingView
- [ ] Portfolio tracking
- [ ] Email alerts for price levels
- [ ] Advanced technical indicators
- [ ] Backtesting engine
- [ ] User accounts and saved analyses
- [ ] Mobile app (React Native)

## Disclaimer

This tool is for **educational and informational purposes only**. It is not financial advice. Always do your own research (DYOR) and consult with a financial advisor before making trading decisions. Cryptocurrency trading carries high risk.

## License

MIT License - Feel free to use and modify for personal or commercial projects.

## Support

For issues or questions:
1. Check troubleshooting section
2. Review API documentation links
3. Check console logs (browser DevTools)
4. Check server logs (terminal)

---

**Built with ❤️ using FastAPI, Gemini AI, and CoinGecko**
