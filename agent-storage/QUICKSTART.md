# Intelligent Inventory Assistant - Quick Start Guide

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv .venv
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
- Copy `.env.example` to `.env`
- Add your OpenAI API key: `OPENAI_API_KEY=sk-...`

### 4. Prepare Database
```bash
python prepare_data.py
```

### 5. Run Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
agent-storage/
├── app.py                 # Streamlit web application
├── agent.py              # LangChain SQL Agent logic
├── prepare_data.py       # Database initialization script
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
├── inventory.db          # SQLite database (generated)
└── README                # Project documentation
```

## Features

- **Natural Language Queries**: Ask questions in plain English
- **Text-to-SQL Translation**: Automatic conversion to SQL queries
- **Business-Oriented Responses**: Natural language results
- **Chat History**: Conversation persistence in session
- **Error Handling**: Graceful error messages

## Test Queries

Try these example questions:
- "What are the names of the products that have less than 20 units in stock?"
- "What is the average unit price of all products in the 'Electronics' category?"
- "What is the total sum of quantity_in_stock for the 'Electronics' category?"
- "How many products are in the 'Accessories' category?"

## Troubleshooting

**Database not found**: Run `python prepare_data.py` first

**API Key error**: Ensure `.env` file exists with valid `OPENAI_API_KEY`

**Connection error**: Check that SQLite and dependencies are properly installed
