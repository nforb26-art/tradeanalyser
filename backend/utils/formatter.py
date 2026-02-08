"""Format trading data with proper decimal places."""

def format_price(value: float, symbol: str = "") -> str:
    """
    Format price to 4 decimal places, or fewer for small values.
    
    Args:
        value: Price value
        symbol: Currency symbol (e.g., "BTC", "USD")
    
    Returns:
        Formatted price string
    """
    if value is None:
        return "N/A"
    
    # For very small values (< 0.0001), use scientific notation or more decimals
    if 0 < value < 0.0001:
        return f"{value:.8f}".rstrip('0').rstrip('.')
    
    # Standard 4 decimal places
    return f"{value:.4f}".rstrip('0').rstrip('.')


def format_percentage(value: float) -> str:
    """Format percentage to 4 decimal places."""
    if value is None:
        return "N/A"
    return f"{value:.4f}%"


def format_analysis(entry: float, stoploss: float, takeprofit: float, symbol: str = "") -> dict:
    """
    Format trading analysis values consistently.
    
    Args:
        entry: Entry point
        stoploss: Stop loss level
        takeprofit: Take profit level
        symbol: Trading pair symbol
    
    Returns:
        Dictionary with formatted values
    """
    return {
        "entry": format_price(entry, symbol),
        "stoploss": format_price(stoploss, symbol),
        "takeprofit": format_price(takeprofit, symbol),
        "risk_reward_ratio": calculate_risk_reward(entry, stoploss, takeprofit)
    }


def calculate_risk_reward(entry: float, stoploss: float, takeprofit: float) -> str:
    """Calculate and format risk/reward ratio."""
    if entry == 0 or stoploss == entry:
        return "N/A"
    
    risk = abs(entry - stoploss)
    reward = abs(takeprofit - entry)
    
    if risk == 0:
        return "N/A"
    
    ratio = reward / risk
    return f"{ratio:.4f}".rstrip('0').rstrip('.')
