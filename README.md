# GroomWise: Your Personalized Skin & Grooming AI Agent

GroomWise is a task-oriented AI agent built with LangChain. It assists users by understanding their skin, hair, and grooming concerns—along with their budget—to recommend suitable self-care products. The agent leverages a Large Language Model (LLM), web search tools, code execution, and a vector memory store for context-aware recommendations.

---
## 🎥 Demo Video Walkthrough

Click below to download or view the GroomWise walkthrough:

▶️ [Watch GroomWise Demo](groomwise-demo.mp4)
---
## 🚀 Agent Architecture & Components

- **LLM:** LLaMA3 via [GROQ](https://console.groq.com/)
- **Agent Type:** `ZERO_SHOT_REACT_DESCRIPTION`
  - **Why:** ReAct agents dynamically choose tools based on instructions and reason step-by-step for answers.
- **Memory:** `FAISS` + `VectorStoreRetrieverMemory`
  - **Why:** Supports long-term memory by storing and recalling previous user questions/responses with semantic search.
- **Tools Used:**
  1. **DuckDuckGoSearchRun**  
     - Search for real-time skincare, haircare, and product info online.
  2. **PythonREPLTool**  
     - Evaluate expressions like price comparisons (e.g., `850 < 1000`) for budget filtering.

---

## 🛠️ Tool Integration & Rationale

| Tool                | Use Case                                                             |
|---------------------|----------------------------------------------------------------------|
| DuckDuckGoSearchRun | Get up-to-date product info and user recommendations from the web.   |
| PythonREPLTool      | Perform calculations for logic such as budget verification.          |
| FAISS + Embeddings  | Store & retrieve past inputs/responses to allow contextual follow-up. |

---

## 🧱 Folder Structure

```bash
groomwise-agent/
 # Streamlit-based frontend 
├── src/
│ ├── init.py
| └── streamlit.py
│ └── groomwise_agent.py # Core agent logic with LLM, tools, memory, and CLI loop
├── memory_index/ # FAISS index folder (auto-generated)
├── .env # API keys
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```
---
## ⚙️ Setup Instructions

1. **Clone Repository**
2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

    ```bash
            pip install -r requirements.txt
            Environment Variables
    ```
4. **Create .env in root**

    ```bash
    GROQ_API_KEY="your_groq_api_key"
    ```
## ▶️ Running GroomWise

1.  **Run the Agent (CLI):**
    ```bash
    python src/groomwise_agent.py
    ```

2.  **Launch the Streamlit Interface (GUI):**
    ```bash
    streamlit run src/streamlit.py
    ```
--

## ✅ Key Features

- 🔍 **Tool Reasoning (ReAct Prompting):**  
  The agent only uses tools (search/calculator) after gathering required context (skin type, concern, and budget).

- 🧠 **Long-Term Memory via FAISS:**  
  Stores and recalls prior user interactions (e.g., past product suggestions) to enable contextual follow-up.

- 🔢 **Budget-Aware Recommendations:**  
  Uses `PythonREPLTool` to ensure product suggestions fall within the user's specified budget.

- 🌐 **Real-Time Search:**  
  `DuckDuckGoSearchRun` allows GroomWise to provide fresh and relevant recommendations from the web.

- 🤖 **LLM Reasoning:**  
  Powered by LLaMA3 via GROQ, providing high-quality natural language understanding and decision-making.

---
## 💡 Known Issues & Future Plans

| Issue / Limitation                                | Planned Improvement                                                   |
|---------------------------------------------------|------------------------------------------------------------------------|
| ❓ Agent doesn't handle vague queries effectively  | Improve prompt parsing and add fuzzy clarification logic               |
| 🔄 No follow-up questions when info is missing     | Inject memory check + custom prompt loop for clarification             |
| 🐢 Slower response time (due to tool chaining)     | Optimize tool usage and reduce unnecessary LLM thinking steps          |
| 🔍 FAISS search is basic                          | Add filters or summarize matches before injecting into prompt          |
| 🔐 No user-based memory persistence yet            | Add user ID/session-based vector store separation                      |


---

## 📐 Architecture Overview

![GroomWise Architecture](./GroomWise.png)

> **Flow:**  
> User input → Streamlit UI / CLI → LangChain Agent → Tools → FAISS (memory recall) → GROQ-powered LLaMA3 LLM  
> → Agent returns contextual and budget-aware recommendations to user as GroomWise’s final answer.

---

## ✨ Credits

- Developed using **LangChain**, **GROQ**, **FAISS**, **HuggingFace**, and **Streamlit**
- Architecture inspired by **tool-use agents**, **ReAct prompting**, and **vector-based memory recall**

---