import streamlit as st
from groomwise_agent import agent_chain, retriever, faiss_store
import os
os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"
st.set_page_config(page_title="GroomWise: Your Grooming Assistant", page_icon="💅", layout="centered")
st.title(" GroomWise")
st.caption("Your AI-powered personal grooming advisor — now with clarifying questions and budget checks!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.chat_input("Tell me about your skin concern, or ask a grooming question...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # Step 1: Recall memory
        memory_snippets = retriever.vectorstore.similarity_search(user_input, k=3)
        recalled_texts = "\n".join([f"- {doc.page_content}" for doc in memory_snippets])
        combined_input = f"{user_input}\n\nRelevant past memory:\n{recalled_texts}"

        # Step 2: Run agent
        response = agent_chain.invoke({"input": combined_input})
        output = response.get("output", " No response from agent.")

        # Step 3: Show agent response
        st.session_state.chat_history.append((user_input, output))
        with st.chat_message("assistant"):
            st.markdown(output)

        # Step 4: Log memory and save store
        print("\n FAISS Memory (Top 3 matches for 'oily skin'):")
        for i, doc in enumerate(retriever.vectorstore.similarity_search("oily skin", k=3)):
            print(f"{i+1}.", doc.page_content)

        faiss_store.save_local("memory_index")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Show full conversation
for user_msg, ai_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(ai_msg)
