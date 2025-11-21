import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
# Assuming agent.py exists in the same folder
from agent import initialize_agent 

# Load environment variables
load_dotenv()

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "inventory.db"

# Page configuration
st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- IMPROVED CSS ---
# We use var(--text-color) and var(--secondary-background-color) 
# so Streamlit handles the switching between Light and Dark modes automatically.
CUSTOM_CSS = """
<style>
    /* Define brand colors that look good in both modes */
    :root {
        --brand-primary: #2E86AB;
        --brand-secondary: #A23B72;
        --brand-accent: #F18F01;
    }

    /* --- HEADER STYLING --- */
    .header-container {
        background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
        color: white; /* Always white text on this gradient */
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        color: white !important;
    }
    
    .subtitle {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.9;
        color: white !important;
        font-weight: 300;
    }

    /* --- SIDEBAR INFO CARD --- */
    .info-card {
        /* Use Streamlit's native secondary background (light gray in light mode, dark gray in dark mode) */
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--brand-primary);
    }
    
    .info-card h3 {
        color: var(--brand-primary) !important;
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .info-card p, .info-card li {
        color: var(--text-color); /* Adapts to Light/Dark automatically */
        font-size: 0.95rem;
    }

    /* --- EXAMPLE QUESTIONS --- */
    .example-item {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        color: var(--text-color);
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        transition: all 0.2s ease;
        font-size: 0.9rem;
    }
    
    .example-item:hover {
        border-color: var(--brand-primary);
        transform: translateX(3px);
    }

    /* --- CHAT INPUT ADJUSTMENT --- */
    /* Clean up the input bottom area without breaking it */
    .stChatInput {
        padding-bottom: 1rem;
    }
    
    /* Optional: Hide the 'Deploy' button if you want a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
"""

@st.cache_resource
def get_agent():
    """Get the initialized LangChain SQL Agent (cached for performance)."""
    try:
        agent_executor = initialize_agent()
        return agent_executor, True
    except Exception as e:
        return str(e), False

def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # --- HEADER ---
    st.markdown("""
        <div class="header-container">
            <div class="main-title">📦 Inventory Management System</div>
            <div class="subtitle">🤖 AI-Powered Natural Language Queries • Real-time Stock Analysis</div>
        </div>
    """, unsafe_allow_html=True)

    if not DATABASE_PATH.exists():
        st.error("⚠️ Database not found! Please run `python create_db.py` first.")
        return
    
    # Initialize agent
    agent_result, success = get_agent()
    
    if not success:
        st.error(f"❌ Failed to initialize the agent. Error: {agent_result}")
        return
    
    agent_executor = agent_result
    
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("### 📊 Dashboard Info")
        
        # Using the CSS class .info-card defined above
        st.markdown("""
            <div class="info-card">
                <h3>About This System</h3>
                <p>This is an AI-powered inventory management assistant that uses natural language processing to query your database.</p>
                <hr style="margin: 10px 0; opacity: 0.2;">
                <p><strong>Features:</strong></p>
                <ul style="padding-left: 20px; margin: 0;">
                    <li>Natural language queries</li>
                    <li>Real-time inventory search</li>
                    <li>SQL query generation</li>
                    <li>Conversation history</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Example Questions")
        examples = [
            "What products have less than 20 units?",
            "Average price of 'Electronics'?",
            "Total stock value?",
            "List all items in Accessories."
        ]
        for example in examples:
            st.markdown(f"""
                <div class="example-item">
                    📦 {example}
                </div>
            """, unsafe_allow_html=True)
    
    # --- Chat Logic ---
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Intelligent Inventory Assistant. Ask me anything about your stock!"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat Input
    user_input = st.chat_input("💬 Ask a question about your inventory...")
    
    if user_input:
        # User message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Assistant response
        with st.spinner("🔄 Processing your question..."):
            try:
                # Invoke agent
                result = agent_executor.invoke({"input": user_input})
                response = result.get("output", "Unable to process the query.")
            except Exception as e:
                response = f"❌ Error: {str(e)}"
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    main()