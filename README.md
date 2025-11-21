# 📦 InvenTell - Intelligent Inventory Agent

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://localhost:8501)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)

> A conversational AI agent that transforms natural language questions into SQL queries for inventory analysis.

---

## 📸 Project Preview

![Project Screenshot](img/image.png)
---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation & Setup

```bash
# 1. Create environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
copy .env.example .env  # Add your OPENAI_API_KEY

# 4. Initialize database
python prepare_data.py

# 5. Launch application

streamlit run app.py
