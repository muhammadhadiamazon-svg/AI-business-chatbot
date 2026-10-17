import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="AI Business Assistant", page_icon="🤖")
st.title("🤖 AI Business Assistant Chatbot")
st.write("Welcome! Ask me anything about our services.")

# Get API key from Streamlit Secrets or Sidebar
api_key = None

# Check Streamlit Secrets (for cloud deployment)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Sidebar fallback (for local testing)
    api_key = st.sidebar.text_input("Apni Gemini API Key Yahan Paste Karein", type="password")

if api_key:
    try:
        client = genai.Client(api_key=api_key)

        # Chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input bar
        if prompt := st.chat_input("Type your message here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # AI response
            with st.chat_message("assistant"):
                response = client.models.generate_content(
                   model="gemini-2.0-flash",
                    contents=prompt,
                )
                reply = response.text
                st.markdown(reply)
                
            st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👈 Chatbot chalane ke liye left sidebar mein apni Gemini API key daalein.")
