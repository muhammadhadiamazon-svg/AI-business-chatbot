import streamlit as st
from google import genai

# Page Config
st.set_page_config(page_title="AI Business Assistant", page_icon="💼", layout="centered")

# Custom CSS Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .main-header {
        font-size: 28px;
        font-weight: 700;
        color: #00adb5;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 16px;
        color: #eeeeee;
        text-align: center;
        margin-bottom: 25px;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Design
st.markdown('<p class="main-header">💼 AI Business Assistant Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Welcome! Apni queries ya file upload karke sawal poochein.</p>', unsafe_allow_html=True)

# Sidebar Branding
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/artificial-intelligence.png", width=120)
    st.title("Business Panel")
    st.write("Aapka apna AI assistant jo files aur text dono samajhta hai.")
    st.markdown("---")
    st.info("💡 Tip: Aap image ya document upload karke us par bhi sawal pooch sakte hain!")

try:
    # Direct Streamlit Secrets se API key lena
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    # File Uploader Feature (Mobile / Computer dono ke liye)
    uploaded_file = st.file_uploader("📂 Koi file select karein (Image/PDF/Text):", type=["jpg", "jpeg", "png", "txt", "pdf"])

    # Chat history initialize
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Purani chat history display karna
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input bar
    if prompt := st.chat_input("Yahan apna sawal likhein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prompts aur Files handle karna
        contents = [prompt]
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            file_part = {
                "mime_type": uploaded_file.type,
                "data": file_bytes
            }
            contents.append(file_part)

        # AI response with fast streaming
        with st.chat_message("assistant"):
            response = client.models.generate_content_stream(
                model="gemini-3.8-flash",
                contents=contents,
            )
            reply = st.write_stream(chunk.text for chunk in response)

        st.session_state.messages.append({"role": "assistant", "content": reply})

except Exception as e:
    st.error(f"API Key Error: Secrets mein 'GEMINI_API_KEY' set honi chahiye. Details: {e}")
