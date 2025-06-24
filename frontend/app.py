import streamlit as st
import requests

st.set_page_config(page_title="AI Support Chatbot", page_icon="🤖")

# Initialize all session state variables up front
for key, default in {
    "messages": [],
    "last_user_prompt": None,
    "last_bot_response": None,
    "feedback_submitted": False,
    "feedback_submit_clicked": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


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
    st.session_state.last_user_prompt = user_prompt
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
            st.session_state.last_bot_response = bot_reply
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.session_state.feedback_submitted = False 
    
    # Initialize feedback_submit_clicked in session_state
if "feedback_submit_clicked" not in st.session_state:
    st.session_state.feedback_submit_clicked = False

# Feedback section
if (
    st.session_state.last_user_prompt
    and st.session_state.last_bot_response
    and not st.session_state.feedback_submitted
    ):
    feedback = st.radio("Was this response helpful?", ["👍", "👎"], key="feedback_radio")

    # Handle feedback submission via session state
    def submit_feedback():
        st.session_state.feedback_submit_clicked = True

    st.button("Submit Feedback", on_click=submit_feedback)

    # After button click is registered
    if st.session_state.feedback_submit_clicked:
        if feedback:
            feedback_data = {
                "feedback": feedback,
                "user_query": st.session_state.last_user_prompt,
                "response": st.session_state.last_bot_response,
            }

            try:
                res = requests.post("http://localhost:8000/feedback", json=feedback_data)
                if res.status_code == 200:
                    st.success("✅ Feedback submitted successfully!")
                    st.session_state.feedback_submitted = True
                    st.session_state.feedback_submit_clicked = False  # Reset
                else:
                    st.error(f"❌ Failed to submit feedback. Status code: {res.status_code}")
                    st.code(res.text)
                    st.session_state.feedback_submit_clicked = False
            except Exception as e:
                st.error("❌ Could not submit feedback.")
                st.exception(e)
                st.session_state.feedback_submit_clicked = False
        else:
            st.warning("⚠️ Please select a feedback option before submitting.")
            st.session_state.feedback_submit_clicked = False
