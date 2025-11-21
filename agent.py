import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
import streamlit as st

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Loading environment variables...")
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") #st.secrets.get("OPENAI_API_KEY") or 
logger.debug(f"OPENAI_API_KEY loaded: {bool(api_key)}")


if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not found. Please check your .env file.")

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "inventory.db"

def case_insensitive_inventory_query(product_name: str, db):
    query = "SELECT * FROM inventory WHERE LOWER(name) = LOWER(?)"
    try:
        result = db._execute(query, (product_name,))
        return result.fetchall()
    except Exception as e:
        return f"Error: {str(e)}"

def initialize_agent():
    """Initialize the LangChain SQL Agent."""
    
    logger.info("Initializing SQL Agent...")
    
    logger.debug("Initializing ChatOpenAI LLM with model: gpt-4o-mini")
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )
        logger.info("ChatOpenAI LLM initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize ChatOpenAI: {str(e)}", exc_info=True)
        raise
    
    logger.debug(f"Connecting to database at: {DATABASE_PATH}")
    try:
        db_url = f"sqlite:///{DATABASE_PATH}"
        logger.debug(f"Database URL: {db_url}")
        db = SQLDatabase.from_uri(db_url)
        logger.info(f"Database connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}", exc_info=True)
        raise
    
    logger.debug("Creating SQLDatabaseToolkit...")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    logger.debug(f"Available tools: {[tool.name for tool in toolkit.get_tools()]}")

    # Add custom case-insensitive inventory query tool as a lambda tool
    
    ci_inventory_tool = Tool(
        name="case_insensitive_inventory_query",
        description="Query inventory table for product names using case-insensitive matching.",
        func=lambda product_name: case_insensitive_inventory_query(product_name, db)
    )
    tools = toolkit.get_tools() + [ci_inventory_tool]

    # Get the prompt template from hub
    logger.debug("Creating SQL Agent prompt template...")
    prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the tool 'case_insensitive_inventory_query' to query product names in the inventory table using case-insensitive matching.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
""")
    logger.debug("Prompt template created successfully")
    # C
    logger.debug("Creating ReAct agent...")
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    logger.debug("ReAct agent created successfully")
    
    # Create agent executor
    logger.debug("Creating AgentExecutor with max_iterations=10...")
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    logger.info("SQL Agent initialized and ready")
    
    return agent_executor

def query_agent(agent_executor, user_query: str) -> str:
    """Execute a query through the agent."""
    logger.info(f"Processing query: {user_query}")
    try:
        logger.debug("Invoking agent executor...")
        result = agent_executor.invoke({"input": user_query})
        output = result.get("output", "Unable to process the query.")
        logger.info(f"Query processed successfully. Output length: {len(output)}")
        logger.debug(f"Query output: {output}")
        return output
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the agent
    agent_executor = initialize_agent()
    print("Agent initialized and ready to process queries.")
    
    # Test queries
    test_queries = [
        "What are the names of the products that have less than 20 units in stock?",
        "What is the average unit price of all products in the 'Electronics' category?",
        "What is the total sum of quantity_in_stock for the 'Electronics' category?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = query_agent(agent_executor, query)
        print(f"Response: {response}")
