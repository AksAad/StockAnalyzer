import streamlit as st
from typing import Dict, List, Optional
import plotly.graph_objects as go
from datetime import datetime

def create_stock_card(stock_data: Dict) -> None:
    """Create a card displaying stock information"""
    with st.container():
        st.markdown("""
            <div class="stCard">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Current Price",
                f"${stock_data['current_price']:,.2f}",
                f"{((stock_data['current_price'] - stock_data['previous_close']) / stock_data['previous_close'] * 100):+.2f}%"
            )
        with col2:
            st.metric("Day High", f"${stock_data['day_high']:,.2f}")
        with col3:
            st.metric("Day Low", f"${stock_data['day_low']:,.2f}")
        
        st.markdown("</div>", unsafe_allow_html=True)

def create_portfolio_summary_card(portfolio_data: Dict) -> None:
    """Create a card displaying portfolio summary"""
    with st.container():
        st.markdown("""
            <div class="stCard">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Portfolio Value", f"${portfolio_data['total_value']:,.2f}")
        with col2:
            st.metric("Cash Balance", f"${portfolio_data['cash_balance']:,.2f}")
        
        st.markdown("</div>", unsafe_allow_html=True)

def create_trade_form(symbol: str, trade_type: str) -> None:
    """Create a form for trading stocks"""
    with st.container():
        st.markdown("""
            <div class="stCard">
        """, unsafe_allow_html=True)
        
        st.subheader(f"{trade_type} {symbol}")
        quantity = st.number_input("Quantity", min_value=1, value=1)
        
        if st.button(f"{trade_type} Stock"):
            st.markdown("</div>", unsafe_allow_html=True)
            return quantity
        
        st.markdown("</div>", unsafe_allow_html=True)
        return None

def create_trade_history_table(trades: List[Dict]) -> None:
    """Create a table displaying trade history"""
    with st.container():
        st.markdown("""
            <div class="stCard">
        """, unsafe_allow_html=True)
        
        # Create DataFrame for better table display
        trade_data = []
        for trade in trades:
            trade_data.append({
                "Date": trade['timestamp'],
                "Symbol": trade['stock_symbol'],
                "Type": trade['trade_type'],
                "Quantity": trade['quantity'],
                "Price": f"${trade['price']:,.2f}",
                "Total": f"${trade['total_value']:,.2f}"
            })
        
        st.table(trade_data)
        st.markdown("</div>", unsafe_allow_html=True)

def create_stock_chart(fig: go.Figure) -> None:
    """Create a container for stock charts"""
    with st.container():
        st.markdown("""
            <div class="stCard">
        """, unsafe_allow_html=True)
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def create_loading_spinner() -> None:
    """Create a loading spinner"""
    with st.spinner("Loading..."):
        st.markdown("""
            <div class="stSpinner"></div>
        """, unsafe_allow_html=True)

def create_success_message(message: str) -> None:
    """Create a success message"""
    st.markdown(f"""
        <div class="stSuccess">
            {message}
        </div>
    """, unsafe_allow_html=True)

def create_error_message(message: str) -> None:
    """Create an error message"""
    st.markdown(f"""
        <div class="stError">
            {message}
        </div>
    """, unsafe_allow_html=True)

def create_navigation_tabs() -> str:
    """Create navigation tabs for different sections"""
    tabs = st.tabs([
        "Dashboard",
        "Trading",
        "Portfolio",
        "Analysis",
        "History"
    ])
    return tabs 