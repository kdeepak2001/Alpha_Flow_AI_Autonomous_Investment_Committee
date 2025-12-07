import yfinance as yf
import sqlite3
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURATION ---
DB_NAME = "market_data.db"
PORTFOLIO = ['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'NVDA', 'AMZN', 'META', 'NFLX'] 

# 1. SETUP DATABASE
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create table for Stock Prices if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS stock_prices
                 (date TEXT, symbol TEXT, close_price REAL, volume INTEGER)''')
    conn.commit()
    conn.close()
    print(f"✅ Database connected: {DB_NAME}")

# 2. FETCH DATA 
def fetch_stock_data(symbol):
    print(f"📉 Fetching data for {symbol}...")
    try:
        stock = yf.Ticker(symbol)
        # Get today's data
        data = stock.history(period="1d")
        
        if not data.empty:
            latest_price = round(data['Close'].iloc[-1], 2)
            latest_volume = int(data['Volume'].iloc[-1])
            today_date = datetime.now().strftime("%Y-%m-%d")
            return today_date, latest_price, latest_volume
        else:
            print(f"⚠️ No data found for {symbol}")
            return None
    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")
        return None

# 3. RUN PIPELINE
def run_pipeline():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    print("🚀 Starting ETL Pipeline...")
    
    for symbol in PORTFOLIO:
        data = fetch_stock_data(symbol)
        if data:
            date, price, volume = data
            # Insert into database
            c.execute("INSERT INTO stock_prices VALUES (?, ?, ?, ?)", 
                      (date, symbol, price, volume))
            print(f"   -> Saved {symbol}: ${price}")
            
    conn.commit()
    conn.close()
    print("🏁 Pipeline finished successfully.")

if __name__ == "__main__":
    run_pipeline()