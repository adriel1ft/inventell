import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
# Garante que a função de inicialização do agente seja importada
from agent import initialize_agent 

# Load environment variables
load_dotenv()

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "inventory.db"

# Page configuration
st.set_page_config(
    page_title="📦 Inventory Management System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definição do CSS embutido (Corrigido e Aprimorado)
CUSTOM_CSS = """
<style>
    /* Main colors */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --success-color: #06A77D;
        --warning-color: #F18F01;
        --danger-color: #C1121F;
        --light-bg: #F5F7FA;
          .stChatInputContainer, .stTextInput, .stTextArea {
        background: transparent !important;
        box-shadow: none !important;
    }
 
    
    /* Global background */
    .main {
        /* Garante que o fundo seja claro e suave */
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 1. Chat input FIX: Remove o fundo e alinha */
    div.stChatInput {
        /* Remove o padding e a margem padrão para grudar na borda inferior */
        margin: 0 !important;
        padding: 0 1rem 0 0 !important; /* Adiciona padding à direita para compensar o layout wide */
        width: 100% !important; 
    }
    /* Remove o fundo branco/cinza do container interno da barra de chat */
    div.stChatInput > div:first-child { 
        background-color: transparent !important; 
        border: none !important;
    }
    
    /* Estilo do Input Text (barra em si) */
    .stChatInput > div > div > div:first-child {
        border-radius: 12px !important;
        border: 2px solid var(--primary-color) !important;
        padding: 8px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        background-color: white !important;
    }
    
    /* Remove a borda redonda do botão de envio */
    .stChatInput button {
        border-radius: 0 !important;
        border: none !important;
        background-color: transparent !important;
        padding: 0 !important;
    }
    
    /* Remove o círculo azul (loading indicator) */
    .stChatInput > div > div > svg {
        display: none !important;
    }
    
    /* Remove qualquer elemento circular desnecessário */
    .stChatInput > div > div > div > svg {
        display: none !important;
    }
    
    /* Header styling */
    .header-container {
        /* Gradiente forte */
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .main-title {
        font-size: 2.8em;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .subtitle {
        font-size: 1.1em;
        margin-top: 0.5em;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Message styling */
    .stChatMessage {
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* User message */
    .stChatMessage:has(.stAvatar:contains("user")) {
        background-color: #E8F4F8; /* Light blue tint */
        border-left: 4px solid var(--primary-color);
    }
    
    /* Assistant message */
    .stChatMessage:has(.stAvatar:contains("assistant")) {
        background-color: #F0E8F8; /* Light purple tint */
        border-left: 4px solid var(--secondary-color);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    /* Info cards */
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-left: 4px solid var(--primary-color);
    }
    
    .info-card h3 {
        color: var(--primary-color);
        margin-top: 0;
    }
    
    /* Examples section */
    .example-item {
        background: #F9FAFB;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 3px solid var(--warning-color);
        transition: all 0.3s ease;
        cursor: pointer; /* Indica que é clicável */
    }
    
    .example-item:hover {
        background: #F0E8F8;
        transform: translateX(5px);
    }
    
    /* Spinner styling */
    .stSpinner {
        color: var(--primary-color) !important;
    }
    
    /* Error/Success messages */
    .stError {
        background-color: #FFE5E5 !important;
        border: 2px solid var(--danger-color) !important;
        border-radius: 8px !important;
    }
    
    .stSuccess {
        background-color: #E5F9F5 !important;
        border: 2px solid var(--success-color) !important;
        border-radius: 8px !important;
    }
</style>
"""

@st.cache_resource
def get_agent():
    """Get the initialized LangChain SQL Agent (cached for performance)."""
    # A função initialize_agent() está no agent.py
    try:
        agent_executor = initialize_agent()
        return agent_executor, True
    except Exception as e:
        # st.error não funciona em funções com cache, então retornamos o erro para ser tratado no main
        return str(e), False

def main():
    # Injeta o CSS customizado
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # --- HEADER ---
    st.markdown("""
        <div class="header-container">
            <div class="main-title">📦 Inventory Management System</div>
            <div class="subtitle">🤖 AI-Powered Natural Language Queries • Real-time Stock Analysis</div>
        </div>
                
    """, unsafe_allow_html=True)
    
    # Check if database exists
    # Usamos Path().exists() para um check mais seguro
    if not DATABASE_PATH.exists():
        st.error("⚠️ Database not found! Please run `python create_db.py` first.")
        return
    
    # Initialize agent
    agent_result, success = get_agent()
    
    if not success:
        # Se falhou, agent_result contém a string de erro
        st.error(f"❌ Failed to initialize the agent. Please check your API key and database configuration. Error: {agent_result}")
        return
    
    # Se sucesso, agent_result é o executor
    agent_executor = agent_result
    
    # --- Sidebar - Info Panel (Visualmente melhorada) ---
    with st.sidebar:
        st.markdown("### 📊 Dashboard Info")
        st.markdown("""
            <div class="info-card">
                <h3>About This System</h3>
                <p>This is an AI-powered inventory management assistant that uses natural language processing to query your database.</p>
                <hr style="border-top: 1px solid #ddd;">
                <p><strong>Features:</strong></p>
                <ul>
                    <li>✅ Natural language queries</li>
                    <li>✅ Real-time inventory search</li>
                    <li><li>✅ SQL query generation</li>
                    <li>✅ Conversation history</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Example Questions")
        examples = [
            "What are the names of the products that have less than 20 units in stock?",
            "What is the average unit price of all products in the 'Electronics' category?",
            "What is the total sum of quantity_in_stock for the 'Electronics' category?",
            "How many products are in the 'Accessories' category?"
        ]
        for i, example in enumerate(examples, 1):
            st.markdown(f"""
                <div class="example-item">
                    <strong>{i}.</strong> {example}
                </div>
            """, unsafe_allow_html=True)
    
    # --- Chat Logic ---
    
    # Initialize session state for conversation history
    if "messages" not in st.session_state:
        # Initial message in English
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your Intelligent Inventory Assistant. Ask me anything about your stock!"}]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=None):
            st.markdown(message["content"])
    
    # User input (mantém o st.chat_input no final para que ele fique fixo)
    user_input = st.chat_input("💬 Ask a question about your inventory...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Redisplay user message
        with st.chat_message("user", avatar=None):
            st.markdown(user_input)
        
        # Generate response
        with st.spinner("🔄 Processing your question..."):
            try:
                # O LangChain 0.2.x usa invoke, que retorna um dicionário
                result = agent_executor.invoke({"input": user_input})
                response = result.get("output", "Unable to process the query.")
            except Exception as e:
                # Tratamento de erro aprimorado
                response = f"❌ Agent Execution Error: Desculpe, não consegui processar a consulta. Tente ser mais específico. Detalhes: {str(e)}"
        
        # Add assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with st.chat_message("assistant", avatar=None):
            st.markdown(response)

if __name__ == "__main__":
    # Carrega variáveis de ambiente aqui, antes de qualquer inicialização
    load_dotenv() 
    main()