import streamlit as st

from groomwise_agent import agent_chain

st.set_page_config(page_title="GroomWise: Your Grooming Assistant", page_icon="💅", layout="centered")
st.title("🤖 GroomWise")
st.caption("Your AI-powered personal grooming advisor — now with clarifying questions and budget checks!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.chat_input("Tell me about your skin concern, or ask a grooming question...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Invoke the agent
    try:
        response = agent_chain.invoke({"input": user_input})
        output = response.get("output", "⚠️ No response from agent.")

        st.session_state.chat_history.append((user_input, output))

        with st.chat_message("assistant"):
            st.markdown(output)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display history
for user_msg, ai_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(ai_msg)
