"""Main FastAPI application for trading pair analysis."""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import sys
from dotenv import load_dotenv
import asyncio
import concurrent.futures

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from api import coingecko, gemini_analysis, newsapi, binance_api, groq_ai, replicate_ai
from api import cryptopanic_news, rss_feeds
from utils import analysis, formatter

app = FastAPI(title="Trade Analyzer", description="Cryptocurrency trading pair analyzer with AI-powered insights")


# Pydantic models
class TradeAnalysisRequest(BaseModel):
    crypto_id: str  # e.g., "bitcoin" or "BTC" or "BTC/USD"
    symbol: str = None  # e.g., "BTC"


class TradeAnalysisResponse(BaseModel):
    pair: str
    price_data: dict
    entry: str
    stoploss: str
    takeprofit: str
    risk_reward: str
    sentiment: dict
    news: list


# Routes
@app.get("/")
async def root():
    """Serve index.html from frontend."""
    return FileResponse("frontend/index.html")


@app.get("/api/search/{query:path}")
async def search_pairs(query: str):
    """Search for cryptocurrency pairs (supports 'BTC', 'BTC/USDT', 'Bitcoin')."""
    try:
        # Clean up query (remove trailing slashes)
        query = query.strip('/').strip()
        
        results = coingecko.search_cryptocurrencies(query)
        
        if not results.get("success", False):
            raise HTTPException(
                status_code=400,
                detail=results.get("error", "Search failed")
            )
        
        return {"success": True, "results": results.get("results", [])}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search error: {str(e)}"
        )


@app.get("/api/trending")
async def get_trending():
    """Get trending cryptocurrencies."""
    try:
        result = coingecko.get_trending_pairs()
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=503,
                detail=result.get("error", "Could not fetch trending")
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Trending error: {str(e)}"
        )


def run_all_ai_analyses(crypto_name: str, price_data: dict) -> dict:
    """
    Run ALL 3 AI analyses in parallel - Gemini, Replicate, Groq.
    Wait for all to complete (with timeout) to ensure all 3 are attempted.
    
    Args:
        crypto_name: Cryptocurrency name
        price_data: Price data dictionary
    
    Returns:
        Dictionary with all AI analyses
    """
    ai_results = {
        "gemini": {"available": False},
        "groq": {"available": False},
        "replicate": {"available": False}
    }
    
    # Run all 3 AIs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            'gemini': executor.submit(gemini_analysis.analyze_trading_pair, crypto_name, price_data),
            'replicate': executor.submit(replicate_ai.analyze_sentiment_replicate, price_data),
            'groq': executor.submit(groq_ai.analyze_sentiment_groq, price_data),
        }
        
        # Wait for all to complete or timeout
        try:
            done, not_done = concurrent.futures.wait(futures.values(), timeout=7)
            
            # Collect all results
            for name, future in futures.items():
                try:
                    if future in done:
                        result = future.result(timeout=1)
                        if result and result.get("available", True):
                            ai_results[name] = result
                except:
                    pass
            
            # Cancel remaining that didn't finish
            for future in not_done:
                future.cancel()
        except:
            pass
    
    return ai_results


def aggregate_ai_sentiments(ai_results: dict) -> dict:
    """
    Aggregate sentiment from multiple AI sources.
    Gemini is the primary source for confidence.
    
    Args:
        ai_results: Dictionary with results from all AIs
    
    Returns:
        Aggregated sentiment and consensus
    """
    sentiments = []
    confidence_sum = 0
    available_count = 0
    gemini_confidence = 5
    
    # Collect all available sentiments
    for ai_name, result in ai_results.items():
        if result.get("available", False):
            available_count += 1
            sentiment = result.get("sentiment", "NEUTRAL").upper()
            
            # Store Gemini's confidence as primary
            if ai_name == "gemini":
                gemini_confidence = result.get("confidence", 5)
            
            # Normalize sentiment values
            if "BUY" in sentiment or "BULLISH" in sentiment:
                sentiments.append(1)
                confidence_sum += result.get("confidence", 5)
            elif "SELL" in sentiment or "BEARISH" in sentiment:
                sentiments.append(-1)
                confidence_sum += result.get("confidence", 5)
            else:
                sentiments.append(0)
    
    # Calculate consensus
    if not sentiments:
        return {
            "consensus": "HOLD",
            "confidence": 0,
            "available_models": 0,
            "warning": "No AI models available"
        }
    
    avg_sentiment = sum(sentiments) / len(sentiments)
    
    # Use Gemini's confidence if available, otherwise average
    if "gemini" in ai_results and ai_results["gemini"].get("available"):
        final_confidence = gemini_confidence
    else:
        final_confidence = confidence_sum / len(sentiments) if sentiments else 5
    
    if avg_sentiment > 0.3:
        consensus = "BUY"
    elif avg_sentiment < -0.3:
        consensus = "SELL"
    else:
        consensus = "HOLD"
    
    return {
        "consensus": consensus,
        "confidence": round(final_confidence, 1),
        "available_models": available_count,
        "average_sentiment": round(avg_sentiment, 2)
    }


@app.post("/api/analyze")
async def analyze_pair(request: TradeAnalysisRequest):
    """
    Analyze a trading pair using multiple APIs and AI models.
    
    Returns entry point, stop loss, take profit, and sentiment from multiple AI sources.
    """
    try:
        # Parse the input (could be "BTC", "BTC/USD", or "bitcoin")
        crypto_query = request.crypto_id or request.symbol
        
        if not crypto_query:
            raise HTTPException(
                status_code=400,
                detail="Error: Please provide either crypto_id or symbol"
            )
        
        # First, try to find the crypto ID
        search_result = coingecko.search_cryptocurrencies(crypto_query)
        
        if not search_result.get("success", False):
            raise HTTPException(
                status_code=404,
                detail=search_result.get("error", "Cryptocurrency not found")
            )
        
        if not search_result.get("results"):
            raise HTTPException(
                status_code=404,
                detail=f"No results found for '{crypto_query}'. Try: BTC, ETH, Bitcoin, Ethereum"
            )
        
        # Get the first (best) match
        best_match = search_result["results"][0]
        crypto_id = best_match["id"]
        display_symbol = best_match["symbol"]
        
        # Get price data from CoinGecko
        price_data = coingecko.get_cryptocurrency_data(crypto_id)
        
        if not price_data.get("success", True):
            raise HTTPException(
                status_code=503,
                detail=price_data.get("error", "Could not fetch cryptocurrency data")
            )
        
        if "error" in price_data and "success" in price_data:
            raise HTTPException(
                status_code=503,
                detail=price_data["error"]
            )
        
        # Calculate base analysis with dynamic stop loss
        base_analysis = analysis.calculate_analysis(price_data)
        
        if "error" in base_analysis:
            raise HTTPException(
                status_code=400,
                detail=f"Analysis error: {base_analysis['error']}"
            )
        
        # Get all AI sentiments
        ai_results = run_all_ai_analyses(best_match["name"], price_data)
        
        # Aggregate sentiments
        aggregated = aggregate_ai_sentiments(ai_results)
        
        # Apply sentiment adjustment
        confidence_score = (aggregated.get("confidence", 5) - 5) / 5.0
        base_analysis = analysis.apply_sentiment_adjustment(base_analysis, confidence_score)
        
        # Format output
        formatted_analysis = formatter.format_analysis(
            base_analysis["entry"],
            base_analysis["stoploss"],
            base_analysis["takeprofit"],
            display_symbol
        )
        
        return {
            "success": True,
            "pair": display_symbol,
            "query": crypto_query,
            "crypto_id": crypto_id,
            "current_price": formatter.format_price(price_data["current_price"]),
            "change_24h": f"{price_data['change_24h']:.2f}%",
            "entry": formatted_analysis["entry"],
            "stoploss": formatted_analysis["stoploss"],
            "takeprofit": formatted_analysis["takeprofit"],
            "risk_reward_ratio": formatted_analysis["risk_reward_ratio"],
            "volatility": base_analysis.get("analysis_basis", {}).get("volatility_level", "UNKNOWN"),
            "volatility_percent": base_analysis.get("analysis_basis", {}).get("volatility", 0),
            "sl_percentage": base_analysis.get("sl_percentage", 2),
            "tp_percentage": base_analysis.get("tp_percentage", 5),
            "sentiment": {
                "consensus": aggregated.get("consensus", "HOLD"),
                "confidence": aggregated.get("confidence", 0),
                "average_sentiment": aggregated.get("average_sentiment", 0),
                "available_models": aggregated.get("available_models", 0),
                "models": {
                    "gemini": {
                        "sentiment": ai_results["gemini"].get("sentiment", "N/A"),
                        "signal": ai_results["gemini"].get("signal", "HOLD"),
                        "confidence": ai_results["gemini"].get("confidence", 0),
                        "available": ai_results["gemini"].get("available", False)
                    },
                    "groq": {
                        "available": ai_results["groq"].get("available", False),
                        "sentiment": ai_results["groq"].get("sentiment", "N/A"),
                        "confidence": ai_results["groq"].get("confidence", 0)
                    },
                    "replicate": {
                        "available": ai_results["replicate"].get("available", False),
                        "sentiment": ai_results["replicate"].get("sentiment", "N/A"),
                        "confidence": ai_results["replicate"].get("confidence", 0)
                    }
                }
            },
            "market_data": {
                "market_cap": formatter.format_price(price_data.get("market_cap", 0)),
                "volume_24h": formatter.format_price(price_data.get("volume_24h", 0)),
                "high_24h": formatter.format_price(price_data.get("high_24h", 0)),
                "low_24h": formatter.format_price(price_data.get("low_24h", 0))
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis error: {str(e)}"
        )


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    # Check API key availability
    api_keys = {
        "gemini": bool(os.getenv("GEMINI_API_KEY")),
        "huggingface": bool(os.getenv("HUGGINGFACE_KEY")),
        "groq": bool(os.getenv("GROQ_KEY")),
        "replicate": bool(os.getenv("REPLICATE_KEY")),
        "newsapi": bool(os.getenv("NEWSAPI_KEY")),
        "binance": True  # No key required
    }
    
    return {
        "status": "healthy",
        "api_keys_configured": api_keys,
        "market_data_sources": ["coingecko", "binance"],
        "ai_models_available": sum([v for k, v in api_keys.items() if k in ["gemini", "groq", "replicate"]]),
        "news_sources": ["newsapi"],
        "total_models": 3,
        "total_news_sources": 1
    }


# Mount static files (CSS, JS)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
