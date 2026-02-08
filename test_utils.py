"""Tests for formatting and analysis utilities."""

import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils import formatter, analysis


class TestFormatter:
    """Test formatter utility functions."""
    
    def test_format_price_standard(self):
        """Test standard price formatting to 4 decimals."""
        assert formatter.format_price(1.23456) == "1.2346"
        assert formatter.format_price(100.99999) == "101"
        assert formatter.format_price(0.5) == "0.5"
    
    def test_format_price_small_values(self):
        """Test formatting for very small values."""
        result = formatter.format_price(0.00000123)
        assert "0.00000123" in result or "1.23e-06" in result
    
    def test_format_price_none(self):
        """Test formatting with None value."""
        assert formatter.format_price(None) == "N/A"
    
    def test_format_percentage(self):
        """Test percentage formatting."""
        assert formatter.format_percentage(5.6789) == "5.6789%"
        assert formatter.format_percentage(-2.3) == "-2.3%"
    
    def test_format_analysis(self):
        """Test full analysis formatting."""
        result = formatter.format_analysis(100, 98, 105)
        assert "entry" in result
        assert "stoploss" in result
        assert "takeprofit" in result
        assert "risk_reward_ratio" in result
    
    def test_calculate_risk_reward(self):
        """Test risk/reward calculation."""
        # Entry: 100, SL: 95, TP: 110
        # Risk: 5, Reward: 10, RR: 2.0
        result = formatter.calculate_risk_reward(100, 95, 110)
        assert float(result) == 2.0


class TestAnalysis:
    """Test analysis utility functions."""
    
    def test_calculate_analysis_basic(self):
        """Test basic analysis calculation."""
        price_data = {
            "current_price": 50000,
            "high_24h": 52000,
            "low_24h": 48000,
            "change_24h": 2.5
        }
        result = analysis.calculate_analysis(price_data)
        
        assert result["entry"] == 50000
        assert result["stoploss"] == 49000  # 2% below
        assert result["takeprofit"] > 50000  # Above entry
    
    def test_calculate_analysis_downtrend(self):
        """Test analysis in downtrend."""
        price_data = {
            "current_price": 50000,
            "high_24h": 52000,
            "low_24h": 48000,
            "change_24h": -5.0
        }
        result = analysis.calculate_analysis(price_data)
        
        assert result["entry"] == 50000
        assert result["stoploss"] < 50000
        # Downtrend should have tighter TP
        assert result["takeprofit"] < 50000 * 1.05
    
    def test_calculate_analysis_zero_price(self):
        """Test analysis with zero price."""
        price_data = {
            "current_price": 0,
            "high_24h": 0,
            "low_24h": 0,
            "change_24h": 0
        }
        result = analysis.calculate_analysis(price_data)
        
        assert result["entry"] is None
        assert result["stoploss"] is None
        assert result["takeprofit"] is None
    
    def test_apply_sentiment_adjustment_bullish(self):
        """Test sentiment adjustment for bullish sentiment."""
        base = {
            "entry": 100,
            "stoploss": 98,
            "takeprofit": 105
        }
        result = analysis.apply_sentiment_adjustment(base, 0.8)
        
        # Bullish should increase takeprofit
        assert result["takeprofit"] > base["takeprofit"]
    
    def test_apply_sentiment_adjustment_bearish(self):
        """Test sentiment adjustment for bearish sentiment."""
        base = {
            "entry": 100,
            "stoploss": 98,
            "takeprofit": 105
        }
        result = analysis.apply_sentiment_adjustment(base, -0.8)
        
        # Bearish should adjust stoploss
        assert result["stoploss"] < base["stoploss"] or result["stoploss"] == base["stoploss"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
