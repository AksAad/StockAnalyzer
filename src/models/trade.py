from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TradeType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    stock_symbol = Column(String, nullable=False)
    trade_type = Column(SQLEnum(TradeType), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(15, 2), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="trades")
    
    def to_dict(self) -> dict:
        """Convert trade to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'stock_symbol': self.stock_symbol,
            'trade_type': self.trade_type,
            'quantity': self.quantity,
            'price': float(self.price),
            'timestamp': self.timestamp.isoformat()
        }
    
    @property
    def total_value(self) -> float:
        """Calculate total value of the trade"""
        return float(self.quantity * self.price)

@dataclass
class TradeCreate:
    user_id: int
    stock_symbol: str
    trade_type: TradeType
    quantity: int
    price: float

@dataclass
class TradeResponse:
    id: int
    user_id: int
    stock_symbol: str
    trade_type: TradeType
    quantity: int
    price: float
    timestamp: datetime
    total_value: float
    
    @classmethod
    def from_trade(cls, trade: Trade) -> 'TradeResponse':
        return cls(
            id=trade.id,
            user_id=trade.user_id,
            stock_symbol=trade.stock_symbol,
            trade_type=trade.trade_type,
            quantity=trade.quantity,
            price=float(trade.price),
            timestamp=trade.timestamp,
            total_value=trade.total_value
        )

@dataclass
class TradeSummary:
    total_buys: float
    total_sells: float
    net_position: float
    trades: list[TradeResponse] 