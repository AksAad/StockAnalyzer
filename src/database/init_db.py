import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

from ..models.user import Base as UserBase
from ..models.portfolio import Base as PortfolioBase
from ..models.trade import Base as TradeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database and create all tables"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get database URL
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///stock_simulator.db")
        logger.info(f"Initializing database at: {os.path.abspath(DATABASE_URL.replace('sqlite:///', ''))}")
        
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Create all tables
        UserBase.metadata.create_all(engine)
        PortfolioBase.metadata.create_all(engine)
        TradeBase.metadata.create_all(engine)
        
        logger.info("Database tables created successfully")
        
        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        return engine, SessionLocal
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def verify_database():
    """Verify database connection and table existence"""
    try:
        engine, SessionLocal = init_database()
        
        # Test connection
        with engine.connect() as conn:
            # Check if tables exist
            tables = engine.table_names()
            required_tables = ['users', 'portfolios', 'trades']
            
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                logger.warning(f"Missing tables: {missing_tables}")
                return False
                
            logger.info("Database verification successful")
            return True
            
    except Exception as e:
        logger.error(f"Database verification failed: {str(e)}")
        return False 