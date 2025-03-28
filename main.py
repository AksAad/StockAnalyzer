import os
import logging
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

from src.models.user import User, UserCreate, UserLogin
from src.models.trade import TradeType
from src.services.trading_service import TradingService
from src.visualization.charts import ChartGenerator
from src.data.stock_data import StockDataManager
from src.ui.theme import apply_custom_theme
from src.ui.components import (
    create_stock_card,
    create_portfolio_summary_card,
    create_trade_form,
    create_trade_history_table,
    create_stock_chart,
    create_loading_spinner,
    create_success_message,
    create_error_message,
    create_navigation_tabs
)
from src.database.db_manager import DatabaseManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize database
db_manager = DatabaseManager()
success, message = db_manager.initialize()

if not success:
    logger.error(f"Database initialization failed: {message}")
    
    # Display detailed error information
    st.error("""
        ### Database Initialization Failed
        
        The application encountered an error while initializing the database. 
        This could be due to:
        
        - Missing or corrupted database file
        - Insufficient permissions
        - Database connection issues
        
        #### Debug Information:
    """)
    
    debug_info = db_manager.get_debug_info()
    st.json(debug_info)
    
    # Provide recovery options
    if st.button("Attempt Database Repair"):
        with st.spinner("Attempting to repair database..."):
            if db_manager._repair_database():
                st.success("Database repair successful! Please refresh the page.")
            else:
                st.error("Database repair failed. Please check the logs for details.")
    
    st.error("""
        If the problem persists, please:
        1. Check the application logs for detailed error messages
        2. Ensure you have write permissions in the application directory
        3. Try manually deleting the database file and restarting the application
    """)
    st.stop()

# Apply custom theme
apply_custom_theme()

def main():
    # Initialize session state
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    # Sidebar for authentication
    with st.sidebar:
        st.header("Authentication")
        
        if st.session_state.user_id is None:
            # Login form
            st.subheader("Login")
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                db = db_manager.get_session()
                try:
                    user = db.query(User).filter(User.username == login_username).first()
                    if user and user.verify_password(login_password):
                        st.session_state.user_id = user.id
                        create_success_message("Login successful!")
                    else:
                        create_error_message("Invalid credentials")
                except Exception as e:
                    logger.error(f"Login error: {str(e)}")
                    create_error_message("An error occurred during login")
                finally:
                    db.close()
            
            # Registration form
            st.subheader("Register")
            reg_username = st.text_input("New Username")
            reg_password = st.text_input("New Password", type="password")
            reg_email = st.text_input("Email")
            
            if st.button("Register"):
                db = db_manager.get_session()
                try:
                    new_user = User(
                        username=reg_username,
                        password_hash=User.hash_password(reg_password),
                        email=reg_email
                    )
                    db.add(new_user)
                    db.commit()
                    create_success_message("Registration successful! Please login.")
                except Exception as e:
                    logger.error(f"Registration error: {str(e)}")
                    create_error_message(f"Registration failed: {str(e)}")
                finally:
                    db.close()
        else:
            if st.button("Logout"):
                st.session_state.user_id = None
                st.experimental_rerun()
    
    # Main content
    if st.session_state.user_id is not None:
        db = db_manager.get_session()
        try:
            trading_service = TradingService(db)
            chart_generator = ChartGenerator()
            stock_data = StockDataManager()
            
            # Get user data
            user = db.query(User).filter(User.id == st.session_state.user_id).first()
            
            # Create navigation tabs
            tabs = create_navigation_tabs()
            
            # Dashboard Tab
            with tabs[0]:
                st.header("Dashboard")
                
                # Portfolio Summary
                portfolio_summary = trading_service.get_portfolio_summary(st.session_state.user_id)
                if portfolio_summary:
                    create_portfolio_summary_card(portfolio_summary)
                    
                    # Portfolio Charts
                    portfolio_chart = chart_generator.create_portfolio_performance_chart(portfolio_summary)
                    if portfolio_chart:
                        create_stock_chart(portfolio_chart)
                    
                    profit_loss_chart = chart_generator.create_profit_loss_chart(portfolio_summary['positions'])
                    if profit_loss_chart:
                        create_stock_chart(profit_loss_chart)
            
            # Trading Tab
            with tabs[1]:
                st.header("Trading")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Buy Stocks")
                    buy_symbol = st.text_input("Stock Symbol (e.g., AAPL)")
                    if buy_symbol:
                        stock_info = stock_data.get_stock_data(buy_symbol)
                        if stock_info:
                            create_stock_card(stock_info)
                            quantity = create_trade_form(buy_symbol, "Buy")
                            if quantity:
                                trade = trading_service.execute_trade(
                                    st.session_state.user_id,
                                    buy_symbol,
                                    TradeType.BUY,
                                    quantity
                                )
                                if trade:
                                    create_success_message(f"Successfully bought {quantity} shares of {buy_symbol}")
                                else:
                                    create_error_message("Failed to execute buy order")
                
                with col2:
                    st.subheader("Sell Stocks")
                    sell_symbol = st.text_input("Stock Symbol to Sell")
                    if sell_symbol:
                        stock_info = stock_data.get_stock_data(sell_symbol)
                        if stock_info:
                            create_stock_card(stock_info)
                            quantity = create_trade_form(sell_symbol, "Sell")
                            if quantity:
                                trade = trading_service.execute_trade(
                                    st.session_state.user_id,
                                    sell_symbol,
                                    TradeType.SELL,
                                    quantity
                                )
                                if trade:
                                    create_success_message(f"Successfully sold {quantity} shares of {sell_symbol}")
                                else:
                                    create_error_message("Failed to execute sell order")
            
            # Portfolio Tab
            with tabs[2]:
                st.header("Portfolio")
                
                portfolio_summary = trading_service.get_portfolio_summary(st.session_state.user_id)
                if portfolio_summary:
                    create_portfolio_summary_card(portfolio_summary)
                    
                    # Portfolio Allocation Chart
                    portfolio_chart = chart_generator.create_portfolio_performance_chart(portfolio_summary)
                    if portfolio_chart:
                        create_stock_chart(portfolio_chart)
            
            # Analysis Tab
            with tabs[3]:
                st.header("Stock Analysis")
                
                analysis_symbol = st.text_input("Enter Stock Symbol for Analysis")
                if analysis_symbol:
                    stock_info = stock_data.get_stock_data(analysis_symbol)
                    if stock_info:
                        create_stock_card(stock_info)
                        
                        # Stock Price Chart
                        price_chart = chart_generator.create_stock_price_chart(analysis_symbol)
                        if price_chart:
                            create_stock_chart(price_chart)
            
            # History Tab
            with tabs[4]:
                st.header("Trade History")
                
                trades = trading_service.get_trade_history(st.session_state.user_id)
                if trades:
                    trade_history_chart = chart_generator.create_trade_history_chart([trade.to_dict() for trade in trades])
                    if trade_history_chart:
                        create_stock_chart(trade_history_chart)
                    
                    create_trade_history_table([trade.to_dict() for trade in trades])
        
        except Exception as e:
            logger.error(f"Application error: {str(e)}")
            create_error_message("An error occurred. Please try again later.")
        finally:
            db.close()
    else:
        st.info("Please login or register to start trading!")

if __name__ == "__main__":
    main() 