import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from ..data.stock_data import StockDataManager

class ChartGenerator:
    def __init__(self):
        self.stock_data = StockDataManager()
    
    def create_stock_price_chart(self, symbol: str, period: str = "1mo") -> Optional[go.Figure]:
        """
        Create a candlestick chart for a stock
        """
        try:
            # Get historical data
            df = self.stock_data.get_historical_data(symbol, period)
            if df is None or df.empty:
                return None
            
            # Create figure with secondary y-axis
            fig = make_subplots(rows=2, cols=1, 
                              shared_xaxes=True,
                              vertical_spacing=0.03,
                              subplot_titles=(f'{symbol} Price', 'Volume'),
                              row_width=[0.7, 0.3])

            # Add candlestick
            fig.add_trace(go.Candlestick(x=df.index,
                                        open=df['Open'],
                                        high=df['High'],
                                        low=df['Low'],
                                        close=df['Close'],
                                        name='OHLC'),
                        row=1, col=1)

            # Add volume bar chart
            fig.add_trace(go.Bar(x=df.index, y=df['Volume'],
                                name='Volume'),
                        row=2, col=1)

            # Update layout
            fig.update_layout(
                title=f'{symbol} Stock Price',
                yaxis_title='Price',
                yaxis2_title='Volume',
                xaxis_rangeslider_visible=False,
                height=800
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating stock chart: {str(e)}")
            return None
    
    def create_portfolio_performance_chart(self, portfolio_data: Dict) -> Optional[go.Figure]:
        """
        Create a pie chart showing portfolio allocation
        """
        try:
            positions = portfolio_data['positions']
            
            # Prepare data for pie chart
            labels = [pos['symbol'] for pos in positions]
            values = [pos['position_value'] for pos in positions]
            
            # Add cash balance
            labels.append('Cash')
            values.append(portfolio_data['cash_balance'])
            
            # Create pie chart
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            
            # Update layout
            fig.update_layout(
                title='Portfolio Allocation',
                height=600
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating portfolio chart: {str(e)}")
            return None
    
    def create_profit_loss_chart(self, positions: List[Dict]) -> Optional[go.Figure]:
        """
        Create a bar chart showing profit/loss for each position
        """
        try:
            # Prepare data
            symbols = [pos['symbol'] for pos in positions]
            profit_loss = [pos['profit_loss'] for pos in positions]
            
            # Create bar chart
            fig = go.Figure(data=[
                go.Bar(
                    x=symbols,
                    y=profit_loss,
                    marker_color=['green' if x >= 0 else 'red' for x in profit_loss]
                )
            ])
            
            # Update layout
            fig.update_layout(
                title='Position Profit/Loss',
                xaxis_title='Stock Symbol',
                yaxis_title='Profit/Loss ($)',
                height=400
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating profit/loss chart: {str(e)}")
            return None
    
    def create_trade_history_chart(self, trades: List[Dict]) -> Optional[go.Figure]:
        """
        Create a line chart showing trade history
        """
        try:
            # Prepare data
            dates = [trade['timestamp'] for trade in trades]
            cumulative_value = []
            current_value = 0
            
            for trade in trades:
                if trade['trade_type'] == 'BUY':
                    current_value -= trade['total_value']
                else:
                    current_value += trade['total_value']
                cumulative_value.append(current_value)
            
            # Create line chart
            fig = go.Figure(data=[
                go.Scatter(
                    x=dates,
                    y=cumulative_value,
                    mode='lines+markers',
                    name='Cumulative P/L'
                )
            ])
            
            # Update layout
            fig.update_layout(
                title='Trade History - Cumulative P/L',
                xaxis_title='Date',
                yaxis_title='Cumulative P/L ($)',
                height=400
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating trade history chart: {str(e)}")
            return None 