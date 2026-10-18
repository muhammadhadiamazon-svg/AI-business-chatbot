import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="AI Business Assistant", page_icon="💼", layout="centered")

# Custom CSS Styling (Aesthetic Gradient Look)
st.markdown("""
    <style>
    /* Cool & Aesthetic Dark Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #090d16 100%);
        color: #f8fafc;
    }
    
    /* Main Header Styling */
    .main-header {
        font-size: 32px;
        font-weight: 800;
        color: #38bdf8;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 0 2px 10px rgba(56, 189, 248, 0.3);
    }
    
    .sub-header {
        font-size: 16px;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Modern Chat Bubble Styling */
    .stChatMessage {
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Header Design
st.markdown('<p class="main-header">💼 AI Business Assistant Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Welcome! Ask any business queries or upload files for analysis.</p>', unsafe_allow_html=True)

# Sidebar Branding
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/artificial-intelligence.png", width=120)
    st.title("Business Panel")
    st.write("Your personal AI assistant capable of processing both text and documents.")
    st.markdown("---")
    st.info("💡 Tip: Upload images or PDFs to ask specific questions about them!")

try:
    # Fetch API key directly from Streamlit Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    # File Uploader Feature
    uploaded_file = st.file_uploader("📂 Select a file (Image/PDF/Text):", type=["jpg", "jpeg", "png", "txt", "pdf"])

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

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
                "mime_type": uploaded_file.type,
                "data": file_bytes
            }
            contents.append(file_part)

        # AI Response with Streaming
        with st.chat_message("assistant"):
            response = client.models.generate_content_stream(
                model="gemini-3.8-flash",
                contents=contents,
            )
            reply = st.write_stream(chunk.text for chunk in response)

        st.session_state.messages.append({"role": "assistant", "content": reply})

except Exception as e:
    st.error(f"API Key Error: 'GEMINI_API_KEY' needs to be set in Secrets. Details: {e}")
