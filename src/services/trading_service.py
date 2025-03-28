from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..models.user import User
from ..models.portfolio import Portfolio, PortfolioCreate, PortfolioUpdate
from ..models.trade import Trade, TradeCreate, TradeType
from ..data.stock_data import StockDataManager

class TradingService:
    def __init__(self, db: Session):
        self.db = db
        self.stock_data = StockDataManager()
    
    def execute_trade(self, user_id: int, stock_symbol: str, trade_type: TradeType, quantity: int) -> Optional[Trade]:
        """
        Execute a trade (buy/sell) for a user
        """
        # Get current stock price
        stock_data = self.stock_data.get_stock_data(stock_symbol)
        if not stock_data:
            return None
            
        current_price = stock_data['current_price']
        
        # Get user
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
            
        # Calculate total cost
        total_cost = quantity * current_price
        
        # Check if user has enough funds for buy
        if trade_type == TradeType.BUY and user.virtual_balance < total_cost:
            return None
            
        # Check if user has enough shares for sell
        if trade_type == TradeType.SELL:
            portfolio = self.db.query(Portfolio).filter(
                Portfolio.user_id == user_id,
                Portfolio.stock_symbol == stock_symbol
            ).first()
            
            if not portfolio or portfolio.quantity < quantity:
                return None
        
        try:
            # Create trade record
            trade = Trade(
                user_id=user_id,
                stock_symbol=stock_symbol,
                trade_type=trade_type,
                quantity=quantity,
                price=current_price
            )
            self.db.add(trade)
            
            # Update user's virtual balance
            if trade_type == TradeType.BUY:
                user.virtual_balance -= total_cost
            else:
                user.virtual_balance += total_cost
            
            # Update portfolio
            portfolio = self.db.query(Portfolio).filter(
                Portfolio.user_id == user_id,
                Portfolio.stock_symbol == stock_symbol
            ).first()
            
            if not portfolio:
                portfolio = Portfolio(
                    user_id=user_id,
                    stock_symbol=stock_symbol,
                    quantity=quantity if trade_type == TradeType.BUY else -quantity,
                    average_price=current_price
                )
                self.db.add(portfolio)
            else:
                if trade_type == TradeType.BUY:
                    # Update average price for buy
                    total_quantity = portfolio.quantity + quantity
                    total_value = (portfolio.quantity * portfolio.average_price) + (quantity * current_price)
                    portfolio.average_price = total_value / total_quantity
                    portfolio.quantity = total_quantity
                else:
                    # For sell, just reduce quantity
                    portfolio.quantity -= quantity
            
            self.db.commit()
            return trade
            
        except IntegrityError:
            self.db.rollback()
            return None
    
    def get_portfolio_summary(self, user_id: int) -> Optional[dict]:
        """
        Get a summary of the user's portfolio
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
            
        portfolios = self.db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
        
        total_value = 0
        positions = []
        
        for portfolio in portfolios:
            # Get current price
            stock_data = self.stock_data.get_stock_data(portfolio.stock_symbol)
            if stock_data:
                current_price = stock_data['current_price']
                position_value = portfolio.quantity * current_price
                total_value += position_value
                
                positions.append({
                    'symbol': portfolio.stock_symbol,
                    'quantity': portfolio.quantity,
                    'average_price': float(portfolio.average_price),
                    'current_price': current_price,
                    'position_value': position_value,
                    'profit_loss': position_value - (portfolio.quantity * float(portfolio.average_price))
                })
        
        return {
            'total_value': total_value,
            'cash_balance': float(user.virtual_balance),
            'positions': positions
        }
    
    def get_trade_history(self, user_id: int, stock_symbol: Optional[str] = None) -> List[Trade]:
        """
        Get user's trade history
        """
        query = self.db.query(Trade).filter(Trade.user_id == user_id)
        if stock_symbol:
            query = query.filter(Trade.stock_symbol == stock_symbol)
        return query.order_by(Trade.timestamp.desc()).all() 