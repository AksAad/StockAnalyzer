from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import yfinance as yf
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Akshat's Stock Analyzer API",
    description="API for the Stock Market Analyzer application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def validate_stock_symbol(symbol: str) -> bool:
    """Validate if the stock symbol exists and is accessible"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return bool(info.get('regularMarketPrice'))
    except Exception as e:
        logger.error(f"Error validating stock symbol {symbol}: {str(e)}")
        return False

def get_stock_info(symbol: str) -> Optional[Dict]:
    """Get stock information with error handling"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        if not info:
            logger.error(f"No info available for stock {symbol}")
            return None
            
        return {
            "symbol": symbol,
            "name": info.get('longName', ''),
            "current_price": info.get('regularMarketPrice', 0),
            "price_change": info.get('regularMarketChange', 0),
            "price_change_percent": info.get('regularMarketChangePercent', 0),
            "volume": info.get('regularMarketVolume', 0),
            "market_cap": info.get('marketCap', 0),
            "pe_ratio": info.get('forwardPE', 0),
            "dividend_yield": info.get('dividendYield', 0)
        }
    except Exception as e:
        logger.error(f"Error getting stock info for {symbol}: {str(e)}")
        return None

def calculate_technical_indicators(hist_data):
    """Calculate technical indicators from historical data"""
    if len(hist_data) < 50:  # Need at least 50 data points for reliable calculations
        return None
        
    closes = hist_data['Close']
    
    # Calculate RSI (14 period)
    delta = closes.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs)).fillna(0)
    
    # Calculate SMAs
    sma_20 = closes.rolling(window=20).mean().fillna(0)
    sma_50 = closes.rolling(window=50).mean().fillna(0)
    
    # Calculate Volatility (20-day standard deviation)
    volatility = closes.pct_change().rolling(window=20).std().fillna(0)
    
    # Calculate Support and Resistance levels
    recent_data = hist_data.tail(20)
    support_level = recent_data['Low'].min()
    resistance_level = recent_data['High'].max()
    
    return {
        "rsi": float(rsi.iloc[-1]),
        "sma_20": float(sma_20.iloc[-1]),
        "sma_50": float(sma_50.iloc[-1]),
        "volatility": float(volatility.iloc[-1]),
        "support_level": float(support_level),
        "resistance_level": float(resistance_level)
    }

@app.get("/stock/{symbol}")
async def get_stock_data(symbol: str, period: str = "1mo") -> Dict:
    """Get current stock data and basic analysis"""
    try:
        if not validate_stock_symbol(symbol):
            raise HTTPException(
                status_code=404,
                detail=f"Stock symbol '{symbol}' not found or not accessible"
            )

        # Get stock info
        stock = yf.Ticker(symbol)
        info = stock.info
        
        if not info:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch stock information for {symbol}"
            )

        # Get historical data based on period
        end_date = datetime.now()
        
        # Map period to timedelta
        period_map = {
            "1d": timedelta(days=1),
            "5d": timedelta(days=5),
            "1mo": timedelta(days=30),
            "3mo": timedelta(days=90),
            "1y": timedelta(days=365),
            "5y": timedelta(days=365 * 5)
        }
        
        start_date = end_date - period_map.get(period, timedelta(days=30))
        
        # For 1d period, use intraday data
        interval = "1m" if period == "1d" else "1d"
        hist = stock.history(start=start_date, end=end_date, interval=interval)
        
        if hist.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No historical data available for {symbol}"
            )
        
        # Calculate technical indicators
        technical_indicators = calculate_technical_indicators(hist)
        
        # Calculate price momentum
        returns = hist['Close'].pct_change()
        momentum = returns.mean() * 252  # Annualized momentum
        
        # Convert historical data to the correct format
        historical_data = []
        for date, row in hist.iterrows():
            historical_data.append({
                'Date': date.strftime('%Y-%m-%d %H:%M:%S') if period == "1d" else date.strftime('%Y-%m-%d'),
                'Close': float(row['Close']),
                'Open': float(row['Open']),
                'High': float(row['High']),
                'Low': float(row['Low']),
                'Volume': int(row['Volume'])
            })
        
        logger.info(f"Fetched {len(historical_data)} data points for {symbol} with period {period}")
        
        # Get additional market data
        market_data = {
            "symbol": symbol,
            "name": info.get('longName', ''),
            "current_price": info.get('regularMarketPrice', 0),
            "price_change": info.get('regularMarketChange', 0),
            "price_change_percent": info.get('regularMarketChangePercent', 0),
            "volume": info.get('regularMarketVolume', 0),
            "avg_volume": info.get('averageVolume', 0),
            "market_cap": info.get('marketCap', 0),
            "pe_ratio": info.get('forwardPE', 0),
            "dividend_yield": info.get('dividendYield', 0),
            "day_high": info.get('dayHigh', 0),
            "day_low": info.get('dayLow', 0),
            "year_high": info.get('fiftyTwoWeekHigh', 0),
            "year_low": info.get('fiftyTwoWeekLow', 0),
            "open": info.get('regularMarketOpen', 0),
            "prev_close": info.get('regularMarketPreviousClose', 0),
            "bid": info.get('bid', 0),
            "ask": info.get('ask', 0),
            "bid_size": info.get('bidSize', 0),
            "ask_size": info.get('askSize', 0),
            "beta": info.get('beta', 0),
            "eps": info.get('trailingEps', 0),
            "sector": info.get('sector', ''),
            "industry": info.get('industry', ''),
            "exchange": info.get('exchange', '')
        }
        
        return {
            **market_data,
            "momentum": momentum,
            "historical_data": historical_data,
            "technical_indicators": technical_indicators
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_stock_data for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stock data: {str(e)}"
        )

@app.get("/stock/{symbol}/analysis")
async def get_stock_analysis(symbol: str) -> Dict:
    """Get detailed technical analysis"""
    try:
        if not validate_stock_symbol(symbol):
            raise HTTPException(
                status_code=404,
                detail=f"Stock symbol '{symbol}' not found or not accessible"
            )

        stock = yf.Ticker(symbol)
        
        # Get historical data for analysis
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No historical data available for {symbol}"
            )
        
        # Calculate technical indicators
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        hist['RSI'] = calculate_rsi(hist['Close'])
        
        # Calculate volatility
        hist['Returns'] = hist['Close'].pct_change()
        volatility = hist['Returns'].std() * (252 ** 0.5)  # Annualized volatility
        
        # Calculate support and resistance levels
        support_level = hist['Low'].rolling(window=20).min().iloc[-1]
        resistance_level = hist['High'].rolling(window=20).max().iloc[-1]
        
        # Calculate additional indicators
        macd = calculate_macd(hist['Close'])
        bollinger_bands = calculate_bollinger_bands(hist['Close'])
        
        # Calculate trend strength
        trend_strength = calculate_trend_strength(hist)
        
        return {
            "symbol": symbol,
            "technical_indicators": {
                "sma_20": float(hist['SMA_20'].iloc[-1]),
                "sma_50": float(hist['SMA_50'].iloc[-1]),
                "rsi": float(hist['RSI'].iloc[-1]),
                "volatility": float(volatility),
                "support_level": float(support_level),
                "resistance_level": float(resistance_level),
                "macd": macd,
                "bollinger_bands": bollinger_bands,
                "trend_strength": float(trend_strength)
            },
            "historical_data": hist.to_dict(orient='records')
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_stock_analysis for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error performing technical analysis: {str(e)}"
        )

@app.get("/market/trending")
async def get_trending_stocks() -> List[Dict]:
    """Get trending stocks based on volume and price movement"""
    try:
        # List of popular stocks to analyze
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA']
        trending = []
        
        for symbol in symbols:
            try:
                stock_info = get_stock_info(symbol)
                if stock_info:
                    trending.append(stock_info)
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {str(e)}")
                continue
        
        # Sort by absolute price change percentage
        trending.sort(key=lambda x: abs(x['price_change_percent']), reverse=True)
        return trending
    except Exception as e:
        logger.error(f"Error in get_trending_stocks: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching trending stocks: {str(e)}"
        )

def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices: pd.Series) -> Dict:
    """Calculate MACD (Moving Average Convergence Divergence)"""
    exp1 = prices.ewm(span=12, adjust=False).mean()
    exp2 = prices.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return {
        "macd": macd.iloc[-1],
        "signal": signal.iloc[-1],
        "histogram": macd.iloc[-1] - signal.iloc[-1]
    }

def calculate_bollinger_bands(prices: pd.Series, period: int = 20) -> Dict:
    """Calculate Bollinger Bands"""
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    return {
        "upper": upper_band.iloc[-1],
        "middle": sma.iloc[-1],
        "lower": lower_band.iloc[-1]
    }

def calculate_trend_strength(hist: pd.DataFrame) -> float:
    """Calculate trend strength using multiple indicators"""
    # Calculate ADX (Average Directional Index)
    high = hist['High']
    low = hist['Low']
    close = hist['Close']
    
    plus_dm = high.diff()
    minus_dm = low.diff()
    
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    
    tr = pd.DataFrame({
        'hl': high - low,
        'hc': abs(high - close.shift(1)),
        'lc': abs(low - close.shift(1))
    }).max(axis=1)
    
    atr = tr.rolling(window=14).mean()
    
    # Calculate trend strength (0-100)
    trend_strength = (abs(plus_dm - minus_dm) / atr).rolling(window=14).mean() * 100
    return trend_strength.iloc[-1]

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 