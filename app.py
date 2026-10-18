import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="AI Business Assistant", page_icon="💼", layout="centered")

# Custom CSS Styling (Ultra Aesthetic & Professional Look)
st.markdown("""
    <style>
    /* Cool & Aesthetic Dark Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b1120;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Main Header Styling */
    .main-header {
        font-size: 32px;
        font-weight: 800;
        color: #38bdf8;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 0 2px 15px rgba(56, 189, 248, 0.4);
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
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(30, 27, 75, 0.25);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Branding & History Panel
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/artificial-intelligence.png", width=100)
    st.title("Business Panel")
    st.write("Your professional AI assistant for text and document intelligence.")
    st.markdown("---")
    
    # Chat History List in Sidebar
    st.subheader("📜 Recent Queries")
    user_queries = [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]
    
    if user_queries:
        for idx, q in enumerate(reversed(user_queries[-10:]), 1):
            short_q = q[:26] + "..." if len(q) > 26 else q
            st.caption(f"{idx}. {short_q}")
            
        st.markdown("---")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    else:
        st.info("No query history yet. Start exploring!")

# Header Design
st.markdown('<p class="main-header">💼 AI Business Assistant Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Welcome! Ask any business queries or upload files for deep analysis.</p>', unsafe_allow_html=True)

try:
    # Fetch API key directly from Streamlit Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    # File Uploader Feature
    uploaded_file = st.file_uploader("📂 Select a file (Image/PDF/Text):", type=["jpg", "jpeg", "png", "txt", "pdf"])

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

        # AI Response with Streaming using recommended model
        with st.chat_message("assistant"):
            response = client.models.generate_content_stream(
                model="gemini-1.5-flash",
                contents=contents,
            )
            reply = st.write_stream(chunk.text for chunk in response)

        st.session_state.messages.append({"role": "assistant", "content": reply})

except Exception as e:
    st.error(f"API Key Error: 'GEMINI_API_KEY' needs to be set in Secrets. Details: {e}")
