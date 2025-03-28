from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import bcrypt
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    virtual_balance = Column(Numeric(15, 2), default=100000.00)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'virtual_balance': float(self.virtual_balance)
        }

@dataclass
class UserCreate:
    username: str
    password: str
    email: str

@dataclass
class UserLogin:
    username: str
    password: str

@dataclass
class UserResponse:
    id: int
    username: str
    email: str
    created_at: datetime
    virtual_balance: float
    
    @classmethod
    def from_user(cls, user: User) -> 'UserResponse':
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            virtual_balance=float(user.virtual_balance)
        ) 