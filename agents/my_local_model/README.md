# 📈 Alpha Flow AI: Autonomous Investment Committee

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![AI Agents](https://img.shields.io/badge/AI-Multi--Agent_System-orange?style=for-the-badge)](https://langchain.com)
[![Status](https://img.shields.io/badge/Status-Active_Development-green?style=for-the-badge)]()

> **An autonomous financial analysis engine where AI agents form a "digital committee" to debate, analyze, and decide on market investments.**

---

## 🖥️ Interactive Demo
Don't just read the code—**interact with the AI Committee!**
*(Once deployed, put your live Streamlit link below)*

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-streamlit-app-link-here)

---

## 🏗️ Architecture
This system mimics a real-world hedge fund investment committee:

![System Architecture](./assets/licensed-image.jpg)

| Agent Name | Role | Responsibility |
| :--- | :--- | :--- |
| **🕵️ The Scout** | Data Ingestion | Scrapes live stock data, news, and 10-K filings. |
| **🧠 The Analyst** | Fundamental Analysis | Processes metrics (P/E, EBITDA) and assesses growth. |
| **⚖️ The Risk Manager** | Risk Control | Evaluates macro headwinds and volatility indices. |
| **🗳️ The Chairman** | Final Decision | Synthesizes all agent reports into a final "Buy/Sell" thesis. |

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/kdeepak2001/Alpha_Flow_AI_Autonomous_Investment_Committee.git](https://github.com/kdeepak2001/Alpha_Flow_AI_Autonomous_Investment_Committee.git)
cd Alpha_Flow_AI_Autonomous_Investment_Committee

## Install Dependencies
pip install -r requirements.txt
3. Launch the Dashboard
We use Streamlit for a modern, interactive UI.
The app will automatically open in your browser at http://localhost:8501