# 🚀 Alpha-Flow AI
## Institutional-Grade Autonomous Investment Committee

**Alpha-Flow** is a next-generation multi-agent financial platform. It bridges the gap between quantitative market data and qualitative fundamental research, leveraging **Retrieval-Augmented Generation (RAG)** to deliver deterministic, citation-backed investment insights.

---

## 🏗️ System Architecture

The platform operates on a **Directed Acyclic Graph (DAG)** architecture. Specialized agents execute in parallel to analyze distinct market dimensions before converging on a final investment thesis.

```mermaid
graph TD
    %% STYLES
    classDef user fill:#212121,stroke:#fff,stroke-width:2px,color:#fff;
    classDef agent fill:#0D47A1,stroke:#000,stroke-width:0px,color:#fff;
    classDef data fill:#1B5E20,stroke:#000,stroke-width:0px,color:#fff;

    %% NODES
    User(👤 Investor):::user
    Manager{👔 Manager Agent}:::agent
    Quant[🧮 Quant Agent]:::agent
    News[📰 Journalist Agent]:::agent
    RAG[🧠 Research Engine]:::agent
    DB[(📂 Vector DB)]:::data
    Web((🌐 Internet)):::data

    %% FLOW
    User -->|Ticker Symbol| Manager
    
    subgraph "Orchestration Layer"
        Manager -->|Trigger| Quant
        Manager -->|Trigger| News
        Manager -->|Trigger| RAG
    end

    Quant -->|SMA & RSI Analysis| Web
    News -->|Sentiment Scraping| Web
    
    subgraph "Knowledge Layer (RAG)"
        RAG <-->|Semantic Retrieval| DB
        DB <-->|Ingest Pipeline| PDF[📄 10-K Reports]
    end
## 📡 Data Pipeline Architecture

The following diagram represents the full lifecycle of data processing inside the Alpha-Flow system — from raw market inputs to final actionable insights.

![Data Pipeline](./assets/data_pipeline.png)

    %% AGGREGATION
    Quant -->|Technical Signal| Manager
    News -->|Sentiment Score| Manager
    RAG -->|Fundamental Context| Manager
    
    Manager -->|Final Investment Thesis| User

## 🛠️ Enterprise Tech Stack

We utilize a high-performance, asynchronous stack designed for data integrity and speed.

| Component        | Technology               | Architectural Decision |
|------------------|---------------------------|-------------------------|
| **LLM Kernel**   | —                         | Superior reasoning, 2M+ token context window. |
| **Orchestration**| Python (Async)            | Parallel, non-blocking execution reduces latency. |
| **Memory (RAG)** | ChromaDB                  | On-device vector storage ensures privacy of financial data. |
| **Embeddings**   | HuggingFace MiniLM-L6-v2  | Dense, low-latency vectorization. |
| **Visualization**| Plotly                    | Interactive OHLC charting for price-action analysis. |
| **Frontend**     | Chainlit                  | React-based conversational UI optimized for agent workflows. |

## ⚡ Engineering Challenges & Solutions

Developing an autonomous financial agent required overcoming several critical system reliability issues.

### **1. The Hallucination Problem**
- ⚠️ **Risk:** LLMs may fabricate financial values.
- ✅ **Solution:** Implemented a strict RAG pipeline restricting outputs to retrieved 10-K filings with citations.

### **2. API Rate Limiting**
- ⚠️ **Risk:** High-frequency queries lead to `429` rate-limit errors.
- ✅ **Solution:** Added local caching and exponential backoff mechanisms inside the QuantAgent to guarantee system stability.

### **3. Pathing & Environment Issues**
- ⚠️ **Risk:** Windows long-path limitations corrupted embedding model files.
- ✅ **Solution:** Built a custom `setup_model.py` that mounts all AI weights into a safe root-level directory:  
  **`C:\ai_cache`**

---

## 🔮 Product Roadmap

We are expanding Alpha-Flow from prototype to Series-A-ready infrastructure.

### **v2.0 — Portfolio Optimization 📈**
Modern Portfolio Theory (MPT) agent enabling Sharpe Ratio–based portfolio rebalancing.

### **v2.5 — Real-Time Intelligence 🌐**
Integration with Serper.dev for **sub-second news analysis** and global event awareness.

### **v3.0 — Voice-First Interface 🎙️**
OpenAI Whisper integration to provide a **hands-free investor assistant** experience.

---

