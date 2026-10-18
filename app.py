import streamlit as st
from google import genai
import pypdf

# Page Configuration
st.set_page_config(
    page_title="AI Business Assistant Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- COOL CUSTOM CSS STYLING ---
custom_css = """
<style>
    /* Main Background & Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0284c7 100%);
        color: #f8fafc;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Cool Headers */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        font-size: 1.1rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Chat Input Box Styling */
    .stChatInput > div {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.2);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #ef4444, #dc2626) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    
    # 1. Multi-Model Support Dropdown
    st.subheader("🤖 Choose AI Model")
    selected_model_name = st.selectbox(
        "Select Model Quality:",
        ["Gemini Flash (Fast)", "Gemini Pro (Deep Reasoning)"],
        index=0
    )
    
    # Map selection to actual working Gemini models
    if "Pro" in selected_model_name:
        model_id = "gemini-2.5-pro"
    else:
        model_id = "gemini-2.5-flash"
        
    st.divider()
    
    # 2. Clear Chat History Button
    st.subheader("🧹 Chat Management")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("⚡ Powered by Google Gemini AI")

# --- MAIN APP LAYOUT ---
st.markdown('<p class="main-title">💼 AI Business Assistant Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Smart Multi-Model Chatbot with Visual & PDF Deep Analysis</p>', unsafe_allow_html=True)

# Helper function to read PDF text
def read_pdf(file):
    pdf_reader = pypdf.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    # File Uploader
    uploaded_file = st.file_uploader(
        "📁 Upload Image or PDF for Analysis:", 
        type=["jpg", "jpeg", "png", "pdf", "txt"]
    )

    # Display Chat History
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Ask anything or analyze your file..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Prepare Content Payload
        contents = [prompt]
        
        if uploaded_file is not None:
            file_type = uploaded_file.type
            file_bytes = uploaded_file.read()
            
            # If PDF or Text File
            if "pdf" in file_type or "text" in file_type:
                if "pdf" in file_type:
                    extracted_text = read_pdf(uploaded_file)
                else:
                    extracted_text = file_bytes.decode("utf-8")
                
                context_prompt = f"\n\n--- Attached Document Context ---\n{extracted_text}\n--- End of Document ---"
                contents[0] = prompt + context_prompt
                
            # If Image File
            elif "image" in file_type:
                file_part = {
                    "inline_data": {
                        "mime_type": file_type,
                        "data": file_bytes
                    }
                }
                contents.append(file_part)

        # AI Response Generation
        with st.chat_message("assistant", avatar="🤖"):
            response = client.models.generate_content_stream(
                model=model_id,
                contents=contents,
            )
            reply = st.write_stream(chunk.text for chunk in response)
            
        st.session_state.messages.append({"role": "assistant", "content": reply})

except Exception as e:
    st.error(f"⚠️ Error: {e}")
