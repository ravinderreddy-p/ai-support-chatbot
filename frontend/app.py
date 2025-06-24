import streamlit as st
import requests

st.set_page_config(page_title="AI Support Chatbot", page_icon="🤖")

st.title("🤖 AI Customer Support Chatbot")
st.markdown("Ask any question related to our services or policies.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            try:
                # Send request to FastAPI backend
                response = requests.post(
                    "http://localhost:8000/chat",  # backend must be running
                    json={"message": user_prompt},
                    timeout=30
                )
                bot_reply = response.json()["response"]
            except Exception as e:
                bot_reply = "❌ Error: Failed to connect to backend."

            st.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
