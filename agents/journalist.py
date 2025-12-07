import yfinance as yf
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load the secret key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: API Key not found. Please check your .env file.")
else:
    genai.configure(api_key=api_key)

class JournalistAgent:
    def analyze_sentiment(self, symbol):
        print(f"📰 Journalist Agent is reading news for {symbol}...")
        
        # 1. Get Headlines
        headlines = self.get_headlines(symbol)
        if not headlines:
            return "NEUTRAL", "No news found."
            
        # 2. Ask Gemini
        print("   -> 🧠 Asking Gemini to analyze sentiment...")
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        You are a financial analyst. Analyze these news headlines for {symbol}:
        {headlines}
        
        Output only a JSON string with this format:
        {{
            "sentiment_score": (number between 0 and 100, where 0 is Panic Selling, 50 is Neutral, 100 is Extreme Greed),
            "summary": "One short sentence explaining why."
        }}
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return "ERROR", "AI failed to analyze."

    def get_headlines(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            news_list = stock.news
            headlines = []
            for n in news_list[:5]:
                if 'content' in n and 'title' in n['content']:
                    headlines.append(n['content']['title'])
                elif 'title' in n:
                    headlines.append(n['title'])
            return headlines
        except:
            return []

if __name__ == "__main__":
    agent = JournalistAgent()
    analysis = agent.analyze_sentiment("TSLA")
    print(analysis)