# Stock Market Simulator

A Python-based stock market simulator that allows users to simulate investing in real-time stock data.

## Features

- Real-time stock data fetching using yFinance API
- Virtual trading system with buy/sell functionality
- Portfolio tracking and analytics
- Data visualization using Matplotlib and Plotly
- User authentication and data persistence
- Performance optimization with caching

## Project Structure

```
stock_market_simulator/
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── stock_data.py
│   │   └── data_cache.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── portfolio.py
│   │   └── trade.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── trading_service.py
│   │   └── analytics_service.py
│   └── visualization/
│       ├── __init__.py
│       └── charts.py
├── database/
│   └── schema.sql
├── tests/
│   └── __init__.py
├── requirements.txt
└── main.py
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Register a new account or login
2. Get virtual money to start trading
3. Search for stocks and view their current prices
4. Place buy/sell orders
5. Track your portfolio performance
6. View analytics and charts

## Contributing

Feel free to submit issues and enhancement requests! 