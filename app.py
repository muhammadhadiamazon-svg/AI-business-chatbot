import streamlit as st
from google import genai

st.set_page_config(page_title="AI Business Assistant", page_icon="🤖")

# Session state initialization for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<p class="main-header">💼 AI Business Assistant Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Welcome! Ask any business queries or upload files for deep analysis.</p>', unsafe_allow_html=True)

try:
    # Fetch API key directly from Streamlit Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    # File Uploader Feature
    uploaded_file = st.file_uploader("Select a file (Image/PDF/Text):", type=["jpg", "jpeg", "png", "txt", "pdf"])

    # Display Previous Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input Bar
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Handle Prompts and Uploaded Files
        contents = [prompt]
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            file_part = {
                "inline_data": {
                    "mime_type": uploaded_file.type,
                    "data": file_bytes
                }
            }
            contents.append(file_part)

        # AI Response with Streaming using recommended model
        with st.chat_message("assistant"):
            response = client.models.generate_content_stream(
                model="gemini-3.8-flash",
                contents=contents,
            )
            reply = st.write_stream(chunk.text for chunk in response)
        
        st.session_state.messages.append({"role": "assistant", "content": reply})

except Exception as e:
    st.error(f"API Key Error: 'GEMINI_API_KEY' needs to be set in Secrets. Details: {e}")
