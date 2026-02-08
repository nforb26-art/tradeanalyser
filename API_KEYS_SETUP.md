# 🚀 Quick API Key Setup Guide

Get your API keys in **20 minutes** and unlock 6 AI models + 5 news sources!

---

## 1️⃣ Groq API (3 minutes)

**What it does:** Lightning-fast AI inference for market sentiment

**Steps:**
1. Go to: https://console.groq.com
2. Click **"Sign Up"**
3. Create account
4. Go to **API Keys** section
5. Create new key
6. Copy the key

**Result:** `gsk_your_key_here`

---

## 2️⃣ Hugging Face API (2 minutes)

**What it does:** Advanced sentiment classification

**Steps:**
1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Name it "Trade Analyzer"
4. Copy the token

**Result:** `hf_your_token_here`

---

## 3️⃣ NewsAPI (2 minutes)

**What it does:** Real-time news sentiment analysis

**Steps:**
1. Go to: https://newsapi.org
2. Click **"Register"** (top right)
3. Create account
4. Copy your API key from dashboard
5. Add to .env

**Result:** `your_newsapi_key_here`

---

## 4️⃣ Cohere API (3 minutes)

**What it does:** Powerful NLP for sentiment classification

**Steps:**
1. Go to: https://cohere.com
2. Click **"Sign Up"**
3. Create account
4. Go to **API Keys**
5. Copy your API key

**Result:** `cohere_your_key_here`

---

## 5️⃣ Replicate API (3 minutes)

**What it does:** Run Llama 2 and other open-source models

**Steps:**
1. Go to: https://replicate.com
2. Click **"Sign In"** or **"Get Started"**
3. Create account
4. Go to **API Tokens**
5. Copy your token

**Result:** `r8_your_token_here`

---

## 6️⃣ Ollama (LOCAL - Completely FREE ✅)

**What it does:** Run AI models locally on your PC (no internet needed after download)

**Steps:**
1. Download: https://ollama.ai
2. Install Ollama
3. Open PowerShell/Terminal and run:
   ```bash
   ollama pull llama2
   ```
4. Keep this running in background:
   ```bash
   ollama serve
   ```
5. Set in .env:
   ```env
   OLLAMA_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

**Note:** First run downloads model (~5GB for llama2). After that, it's instant!

---

## 7️⃣ Binance API (FREE - No Key Required ✅)

**What it does:** Live exchange data, order book, trading volume

**No setup needed!** Binance is free and public, no API key required.

---

## 8️⃣ Kraken API (FREE - No Key Required ✅)

**What it does:** Alternative exchange data, bid-ask spreads, depth

**No setup needed!** Kraken is free and public, no API key required.

---

## 9️⃣ CryptoPanic (FREE - No Key Required ✅)

**What it does:** Crypto-specific news with community sentiment voting

**No setup needed!** CryptoPanic is free and public.

---

## 🔟 RSS Feeds (FREE - No Key Required ✅)

**What it does:** Latest news from CoinDesk, Cointelegraph, Messari

**No setup needed!** All RSS feeds are free and public.

---

## 🔧 Adding Keys to `.env`

1. **Open .env file:**
   ```bash
   cd "c:\Users\estate boss\Documents\trade analyser"
   ```
   Find and open `.env` file (use Notepad or VS Code)

2. **Fill in your keys:**
   ```env
   GEMINI_API_KEY=AIzaSyDO02zA8zmoPyZFvEnVuJYfl2dZ3FVtHkY
   NEWSAPI_KEY=bf713565c57344c6a3c751d77743b412
   GROQ_KEY=your_groq_key_here
   HUGGINGFACE_KEY=your_hf_token_here
   TOGETHER_KEY=your_together_key_here
   MISTRAL_KEY=your_mistral_key_here
   ALPHAVANTAGE_KEY=your_alphavantage_key_here
   ```

3. **Save the file**

4. **Restart the server:**
   ```bash
   python backend/main.py
   ```

---

## ✅ Verify It Works

**Test in browser:**
1. Open: http://localhost:8000
2. Search: "BTC/USD"
3. Check results show:
   - ✓ All 6 AI models (or however many you configured)
   - ✓ Consensus sentiment
   - ✓ Volatility info
   - ✓ Dynamic stop loss

**Test in terminal:**
```bash
# Should show healthy status with configured models
curl http://localhost:8000/api/health
```

---

## 🎯 Which APIs Are Required?

| API | Required? | Impact |
|-----|-----------|--------|
| Gemini | No | AI sentiment analysis |
| Groq | No | Fast AI inference |
| Hugging Face | No | Diverse analysis |
| Cohere | No | NLP sentiment classification |
| Replicate | No | Llama 2 reasoning |
| Ollama | No | Local AI (no internet) |
| NewsAPI | No | General news sentiment |
| CryptoPanic | ✅ FREE | Crypto-specific news |
| RSS Feeds | ✅ FREE | CoinDesk, Cointelegraph, Messari |
| Binance | ✅ FREE | Live market data |
| Kraken | ✅ FREE | Alternative price data |

**Recommended Starting Setup:**
1. **AI Models:** Gemini + Groq + Hugging Face (3 fast APIs)
2. **News:** CryptoPanic (crypto-specific) + NewsAPI (general)
3. **Market Data:** Binance + Kraken (already working!)
4. **Optional:** Cohere + Replicate + Ollama for enhanced analysis

**Quick Start (ZERO API keys needed):**
- CoinGecko + Binance + Kraken (market data) ✅
- Gemini (already configured) ✅
- CryptoPanic + NewsAPI + RSS feeds ✅
- **Everything works completely FREE!**

---

## 🆘 Troubleshooting

### "API key not configured"
- Check `.env` file is in the right directory
- Make sure you didn't forget any keys
- Restart server after editing .env

### "API error: unauthorized"
- Double-check your API key is correct
- Try generating a new key
- Make sure it's not expired

### "Request timeout"
- API server might be slow
- Try again in a few seconds
- Check your internet connection

### "Only 3 models showing?"
- That's normal! Add more API keys over time
- Each configured model improves accuracy
- At least Gemini or Groq is recommended

---

## 📊 What You Get With Each API

### Gemini (Free)
```json
{
  "sentiment": "BULLISH",
  "signal": "BUY",
  "confidence": 8,
  "explanation": "Strong uptrend..."
}
```

### Groq (Free)
```json
{
  "sentiment": "BUY",
  "confidence": 9,
  "reason": "Volume spike with price increase..."
}
```

### Hugging Face (Free)
```json
{
  "sentiment": "BULLISH",
  "confidence": 0.95
}
```

### Together.ai (Free)
```json
{
  "sentiment": "BUY",
  "analysis": "Price action shows strong support..."
}
```

### Mistral (Free)
```json
{
  "sentiment": "BULLISH",
  "score": 8,
  "reasoning": "Multiple bullish indicators..."
}
```

---

## 🎓 Example Scenario

You configured all 5 APIs:

```
User: Analyzes "BTC/USD"

System Response:
┌─────────────────────────────────────┐
│ Consensus: BUY                      │
│ Confidence: 8.2/10                  │
│ Models: 5/5 Available               │
├─────────────────────────────────────┤
│ Gemini:      BULLISH ✓              │
│ Groq:        BUY ✓                  │
│ Hugging Face: BULLISH ✓             │
│ Together:    BUY ✓                  │
│ Mistral:     BULLISH ✓              │
├─────────────────────────────────────┤
│ Entry:       $45,234.5678           │
│ Stop Loss:   $43,574.98 (3.7% SL)  │
│ Take Profit: $47,496.42 (5.0% TP)  │
│ Volatility:  MEDIUM (4.2%)          │
└─────────────────────────────────────┘
```

---

## 💡 Pro Tips

1. **Start with Groq** - It's the fastest
2. **Add Mistral next** - Best detailed analysis
3. **HuggingFace** - Great for sentiment
4. **Together.ai** - Open-source approach
5. **Gemini** - Always good baseline

---

## 🚀 You're All Set!

Once you have 2+ API keys:
1. Add them to `.env`
2. Run server: `python backend/main.py`
3. Open: http://localhost:8000
4. Start analyzing with 5 AI models!

---

**Total setup time: ~15 minutes**
**AI models active: 5+ (depending on keys)**
**Prediction accuracy: Dramatically improved! 📈**

Good luck! 🎉
