# -- Importing Libraries --
import os
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools import PythonREPLTool
from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq

# Load env variables
load_dotenv()
if os.getenv("GROQ_API_KEY") is None:
    print("GROQ_API_KEY not found in .env. Please add it.")
    exit()

# -- LLM from GROQ --
llm = ChatGroq(
    model="llama3-8b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)
# -- Tools --
python_tool = PythonREPLTool(
    globals={},
    locals={"__builtins__": {"print": print, "len": len, "min": min, "max": max}}
)
search_tool = DuckDuckGoSearchRun()
tools = [search_tool, python_tool]

# -- FAISS Memory Setup --
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
if os.path.exists("memory_index"):
    faiss_store = FAISS.load_local("memory_index", embedding_model, allow_dangerous_deserialization=True)

else:
    faiss_store = FAISS.from_texts(["dummy memory initialization"], embedding_model)

retriever = faiss_store.as_retriever(search_kwargs={"k": 5})
memory = VectorStoreRetrieverMemory(retriever=retriever, memory_key="chat_history")

# -- Prompt Template --
tool_names = ", ".join([tool.name for tool in tools])
tool_descriptions = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])

prompt = PromptTemplate.from_template(f"""
You are GroomWise — a polite, intelligent personal grooming advisor that helps users select skincare, haircare, and wellness products based on their needs.

 Your mission:
- ALWAYS understand the user's skin type, concern, and budget BEFORE using tools.
- DO NOT answer or search blindly. First, gather enough context.
- If the input is vague (e.g., "Suggest something for my face" or "I have oily skin"), politely ask for clarification.

 NEVER use DuckDuckGoSearchRun or Python_REPL until:
1. You know the user's skin/hair type.
2. You understand the concern (e.g., acne, dark circles).
3. You know the budget or have verified it's not needed.

✅ Once you have this info, proceed using the following ReAct reasoning format:

---

**TOOL INSTRUCTION FORMAT**

Thought: Describe what you're thinking and why  
Action: One of [{tool_names}]  
Action Input: The input string for the tool  
Observation: Result from the tool  
... (You can repeat Thought/Action/Observation)  
Final Answer: Your final recommendation with reasoning  

---

**Example 1 (Clarification First):**

Question: I have oily skin.  
Thought: The user mentioned a skin type but didn’t give a budget or a specific concern.  
Final Answer: Could you please tell me more — do you have any specific concern like acne or dark circles? And what’s your budget?  

---

**Example 2 (Tool Use After Info):**

Question: I have oily skin and acne. My budget is under 1000 PKR.  
Thought: I have all needed info. I’ll search for suitable products.  
Action: DuckDuckGoSearchRun  
Action Input: best face wash for oily acne-prone skin under 1000 PKR in Pakistan  
Observation: [Search results]  
Thought: I need to check if prices fit the budget.  
Action: Python_REPL  
Action Input: 850 < 1000  
Observation: True  
Final Answer: Product A is under your budget and works for oily skin and acne.  

---

TOOLS:  
{tool_descriptions}  

Begin!  

Question: {{input}}  
{{agent_scratchpad}}  
""")

# -- Agent Initialization --
agent_chain = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
    agent_kwargs={"system_message": prompt.template}
)

# -- CLI Runner --
def run_groomwise_agent():
    print("🤖 GroomWise Agent (Tool-Enforced ReAct Mode) Ready!")
    print("   (Type 'exit' to end the conversation)")
    while True:
        try:
            user_input = input("👤 You: ")
            if user_input.lower() == 'exit':
                print(" GroomWise: Farewell, radiant one.")
                break

            # Retrieve relevant past memory
            memory_snippets = retriever.vectorstore.similarity_search(user_input, k=3)
            recalled_texts = "\n".join([f"- {doc.page_content}" for doc in memory_snippets])
            combined_input = f"{user_input}\n\nRelevant past memory:\n{recalled_texts}"

            # Invoke the agent
            response = agent_chain.invoke({"input": combined_input})
            print(f" GroomWise: {response['output']}")

            # Debug: Show memory
            print("\n FAISS Memory (Top 3 matches for 'oily skin'):")
            for i, doc in enumerate(retriever.vectorstore.similarity_search("oily skin", k=3)):
                print(f"{i+1}.", doc.page_content)

            # Save memory
            faiss_store.save_local("memory_index")

        except Exception as e:
            print(f" An error occurred: {e}")
            break

if __name__ == "__main__":
    print("✅ GROQ API Loaded:", os.getenv("GROQ_API_KEY"))
    run_groomwise_agent()
    