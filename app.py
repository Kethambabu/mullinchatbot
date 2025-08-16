import streamlit as st
from chatbot import client

st.set_page_config(page_title="Multilingual Chatbot", layout="centered")
st.title("🌍 Multilingual Chatbot (Groq + Streamlit)")

# Sidebar language selection
lang = st.sidebar.selectbox(
    "Choose Language",
    options=["English", "Hindi", "Spanish", "French", "German", "Chinese"],
    index=0
)

# Chat history initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("Enter your message")

# On send
if st.button("Send") and user_input:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare full message list with a strong language directive
    system_instruction = {
        "role": "system",
        "content": f"You are a multilingual assistant. Always respond only in {lang}, no matter what language the user uses."
    }
    messages = [system_instruction] + st.session_state.chat_history

    # Call Groq LLM
    with st.spinner("Thinking..."):
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )
        reply = completion.choices[0].message.content.strip()

    # Add assistant reply to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Display conversation
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💬 **You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"🤖 **Bot:** {msg['content']}")

# Clear chat option
if st.sidebar.button("🔄 New Chat"):
    st.session_state.chat_history = []
    st.rerun()
