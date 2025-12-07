from QuantAgent import QuantAgent
from journalist import JournalistAgent
import json

class ManagerAgent:
    def make_decision(self, symbol):
        print(f"\n👔 Manager Agent is reviewing {symbol}...")
        
        # 1. Get Technical Analysis (Quant)
        quant = QuantAgent()
        quant_signal = quant.analyze(symbol)
        
        # 2. Get News Sentiment (Journalist)
        journalist = JournalistAgent()
        news_response = journalist.analyze_sentiment(symbol)
        
        # 3. Parse the JSON from the Journalist
        try:
            # Clean up the string (remove ```json and ``` if they exist)
            clean_json = news_response.replace("```json", "").replace("```", "").strip()
            news_data = json.loads(clean_json)
            
            sentiment_score = news_data.get("sentiment_score", 50)
            summary = news_data.get("summary", "No summary provided.")
        except Exception as e:
            print(f"⚠️ Error parsing news JSON: {e}")
            sentiment_score = 50
            summary = "Could not analyze news."

        print(f"   -> Quant Signal: {quant_signal}")
        print(f"   -> News Sentiment: {sentiment_score}/100")
        
        # 4. THE FINAL DECISION LOGIC
        final_verdict = "HOLD ✋"
        
        # Logic: Combining Technicals + Fundamentals
        if "BUY" in quant_signal and sentiment_score > 70:
            final_verdict = "STRONG BUY 🚀 (Technicals + News Agree)"
        elif "BUY" in quant_signal and sentiment_score > 50:
            final_verdict = "BUY ✅ (Technicals Good, News Neutral)"
        elif "SELL" in quant_signal and sentiment_score < 30:
            final_verdict = "STRONG SELL 📉 (Technicals + News Agree)"
        elif "SELL" in quant_signal and sentiment_score < 50:
            final_verdict = "SELL ❌ (Technicals Bad, News Neutral)"
        elif sentiment_score > 85:
            final_verdict = "SPECULATIVE BUY 🎰 (News is Hype, but Technicals Weak)"
            
        print(f"\n🏆 FINAL COMMITTEE DECISION for {symbol}: {final_verdict}")
        print(f"   📝 Reason: {summary}\n")
        
        return final_verdict

# --- TEST THE BOSS ---
if __name__ == "__main__":
    boss = ManagerAgent()
    boss.make_decision("TSLA")