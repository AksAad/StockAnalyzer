from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = 'portfolios'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    stock_symbol = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    average_price = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="portfolios")
    
    def to_dict(self) -> dict:
        """Convert portfolio to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'stock_symbol': self.stock_symbol,
            'quantity': self.quantity,
            'average_price': float(self.average_price),
            'created_at': self.created_at.isoformat()
        }
    
    @property
    def total_value(self) -> float:
        """Calculate total value of the portfolio position"""
        return float(self.quantity * self.average_price)

@dataclass
class PortfolioCreate:
    user_id: int
    stock_symbol: str
    quantity: int
    average_price: float

@dataclass
class PortfolioUpdate:
    quantity: int
    average_price: float

@dataclass
class PortfolioResponse:
    id: int
    user_id: int
    stock_symbol: str
    quantity: int
    average_price: float
    created_at: datetime
    total_value: float
    
    @classmethod
    def from_portfolio(cls, portfolio: Portfolio) -> 'PortfolioResponse':
        return cls(
            id=portfolio.id,
            user_id=portfolio.user_id,
            stock_symbol=portfolio.stock_symbol,
            quantity=portfolio.quantity,
            average_price=float(portfolio.average_price),
            created_at=portfolio.created_at,
            total_value=portfolio.total_value
        )

@dataclass
class PortfolioSummary:
    total_value: float
    positions: List[PortfolioResponse]
    cash_balance: float 