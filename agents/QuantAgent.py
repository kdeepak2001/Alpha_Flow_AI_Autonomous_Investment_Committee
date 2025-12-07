import yfinance as yf
import pandas as pd

class QuantAgent:
    def analyze(self, symbol):
        print(f"🧮 Quant Agent is analyzing {symbol}...")
        
        # 1. Fetch 1 Month of Data to calculate averages
        stock = yf.Ticker(symbol)
        df = stock.history(period="1mo")
        
        if df.empty:
            print(f"⚠️ No data for {symbol}")
            return "NEUTRAL"
            
        # 2. CALCULATION (The Pandas "Transform" Skill)
        # Calculate the 20-Day Simple Moving Average (SMA)
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        
        # Get the latest values
        current_price = df['Close'].iloc[-1]
        sma_20 = df['SMA_20'].iloc[-1]
        
        # Handle missing data (NaN)
        if pd.isna(sma_20):
            sma_20 = current_price 
            
        # 3. THE DECISION LOGIC
        signal = "NEUTRAL"
        if current_price > sma_20:
            signal = "BUY (Price is above 20-day Average)"
        elif current_price < sma_20:
            signal = "SELL (Price is below 20-day Average)"
            
        print(f"   -> Price: ${current_price:.2f} | SMA (20-day): ${sma_20:.2f}")
        print(f"   -> Quant Decision: {signal}")
        
        return signal

# --- TEST THE AGENT ---
if __name__ == "__main__":
    agent = QuantAgent()
    # Test with Apple
    agent.analyze("AAPL")