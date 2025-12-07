import chainlit as cl
from QuantAgent import QuantAgent
from journalist import JournalistAgent
from rag_engine import RAGEngine
import yfinance as yf
import plotly.graph_objects as go
import json

# --- 1. GLOBAL SETUP ---
print("⏳ System Startup: Loading Neural Neural Memory...")
try:
    brain = RAGEngine()
    print("✅ System Startup: Knowledge Base Loaded.")
except:
    brain = None

# --- 2. LOGIC ENGINE ---
async def run_manager_logic(symbol):
    """Core logic to run the debate."""
    # A. Quant
    quant = QuantAgent()
    quant_signal = await cl.make_async(quant.analyze)(symbol)
    
    # B. Journalist
    journalist = JournalistAgent()
    news_response = await cl.make_async(journalist.analyze_sentiment)(symbol)
    
    try:
        clean_json = news_response.replace("```json", "").replace("```", "").strip()
        news_data = json.loads(clean_json)
        score = news_data.get("sentiment_score", 50)
        reason = news_data.get("summary", "Analysis unavailable.")
    except:
        score = 50
        reason = "Could not parse news data."

    # C. Decision
    verdict = "HOLD ✋"
    if "BUY" in quant_signal and score > 70: verdict = "STRONG BUY 🚀"
    elif "BUY" in quant_signal and score > 50: verdict = "BUY ✅"
    elif "SELL" in quant_signal and score < 30: verdict = "STRONG SELL 📉"
    elif "SELL" in quant_signal and score < 50: verdict = "SELL ❌"
    
    return verdict, reason, score, quant_signal

# --- 3. UI CONFIGURATION ---

@cl.set_starters
async def set_starters():
    """Defines the clickable buttons for new users."""
    return [
        cl.Starter(
            label="Analyze Tesla (TSLA)",
            message="TSLA",
            icon="/public/logo_dark.png", # Uses your logo if available, or default
            ),
        cl.Starter(
            label="Check Apple (AAPL) Risks",
            message="AAPL",
            icon="/public/logo_dark.png",
            ),
        cl.Starter(
            label="Evaluate Microsoft (MSFT)",
            message="MSFT",
            icon="/public/logo_dark.png",
            ),
        cl.Starter(
            label="Explain the Tech Stack",
            message="Explain how this AI works.",
            icon="/public/logo_dark.png",
            )
    ]

@cl.on_chat_start
async def start():
    """Welcome Message."""
    await cl.Message(
        content="""
# 👋 **Alpha-Flow AI**
### Institutional-Grade Investment Committee

I am an autonomous agent system that combines **Technical Analysis**, **News Sentiment**, and **Fundamental Research (RAG)**.

**Capabilities:**
* 📈 **Quant Agent:** 20-Day SMA & Trend Analysis
* 📰 **Journalist Agent:** Live News Sentiment Scanning
* 🧠 **Research Agent:** Deep-dive into 10-K Reports
        """
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Main Chat Loop."""
    
    # Handle the "Explain Tech Stack" starter separately
    if "how this ai works" in message.content.lower():
        await cl.Message(content="**I run on a Multi-Agent Architecture:**\n1. **Quant Agent:** Python/Pandas for math.\n2. **Journalist Agent:** Gemini Pro for news reading.\n3. **Memory:** ChromaDB Vector Database for reading PDFs.").send()
        return

    symbol = message.content.upper().strip()
    
    # Start the analysis UI
    await cl.Message(content=f"🤖 **Activating Agents for {symbol}...**").send()
    
    async with cl.Step(name="Committee Debate", type="run") as step:
        step.input = f"Gathering intelligence on {symbol}..."
        
        # Run Logic
        verdict, reason, score, signal = await run_manager_logic(symbol)
        
        # Run RAG
        rag_insight = "No internal research available."
        if brain:
            query = f"What are the key risks and growth drivers for {symbol}?"
            results = await cl.make_async(brain.search)(query)
            if results:
                rag_insight = "\n".join([f"• {r[:200]}..." for r in results[:3]])
        
        step.output = "Analysis Complete."

    # Final Report
    report = f"""
    # 🏆 Verdict: **{verdict}**
    
    ### 📊 Agent Findings
    * **Technical:** {signal}
    * **Sentiment:** {score}/100 ({reason})
    
    ---
    ### 🧠 Internal Research (RAG)
    > {rag_insight}
    """
    
    # Chart
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="6mo")
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(title=f"{symbol} Performance", xaxis_title="Date", yaxis_title="Price")
        
        await cl.Message(content=report).send()
        await cl.Message(content="**Price Action:**", elements=[cl.Plotly(name="chart", figure=fig, display="inline")]).send()
    except:
        await cl.Message(content=f"⚠️ Market data unavailable for {symbol}").send()