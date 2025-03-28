import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDataManager:
    def __init__(self, cache_duration: int = 300):  # 5 minutes default cache
        self.cache_duration = cache_duration
        self._cache: Dict[str, Dict] = {}
        
    def get_stock_data(self, symbol: str) -> Optional[Dict]:
        """
        Fetch stock data with caching
        """
        current_time = datetime.now()
        
        # Check cache first
        if symbol in self._cache:
            cached_data = self._cache[symbol]
            if (current_time - cached_data['timestamp']).seconds < self.cache_duration:
                return cached_data['data']
        
        try:
            # Fetch new data
            stock = yf.Ticker(symbol)
            info = stock.info
            
            if not info:
                logger.error(f"No data found for symbol {symbol}")
                return None
                
            data = {
                'symbol': symbol,
                'name': info.get('longName', ''),
                'current_price': info.get('currentPrice', 0.0),
                'market_cap': info.get('marketCap', 0),
                'volume': info.get('volume', 0),
                'day_high': info.get('dayHigh', 0.0),
                'day_low': info.get('dayLow', 0.0),
                'previous_close': info.get('previousClose', 0.0),
                'timestamp': current_time
            }
            
            # Update cache
            self._cache[symbol] = {
                'data': data,
                'timestamp': current_time
            }
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_historical_data(self, symbol: str, period: str = "1mo") -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data
        """
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)
            return df
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {str(e)}")
            return None
    
    def search_stocks(self, query: str) -> list:
        """
        Search for stocks based on company name or symbol
        """
        try:
            # Using yfinance's search functionality
            stocks = yf.Tickers(query)
            results = []
            
            for symbol in stocks.tickers:
                info = stocks.tickers[symbol].info
                if info:
                    results.append({
                        'symbol': symbol,
                        'name': info.get('longName', ''),
                        'exchange': info.get('exchange', '')
                    })
            
            return results
        except Exception as e:
            logger.error(f"Error searching stocks: {str(e)}")
            return []
    
    def clear_cache(self):
        """
        Clear the data cache
        """
        self._cache.clear() 