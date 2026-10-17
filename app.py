import streamlit as st
from google import genai

# Page Title
st.set_page_config(page_title="AI Business Assistant", page_icon="🤖")
st.title("🤖 AI Business Assistant Chatbot")
st.write("Welcome! Ask me anything about our services.")

# Embedded API Key
API_KEY = "AQ.Ab8RN6L3C20x4vpCcozGFpSYazja6f4DMkX5shCF9F4wavdPSw"
client = genai.Client(api_key=API_KEY)

# Chat history initialize karna
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input bar
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response generate karna
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        reply = response.text
        st.markdown(reply)
        
    st.session_state.messages.append({"role": "assistant", "content": reply})