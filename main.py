import os 
from dotenv import load_dotenv
import streamlit as st
import google.genai as genai

load_dotenv()

st.set_page_config(
    page_title="Geminie ChatBot", 
    page_icon="🤖", 
    layout= "centered"
)

def get_api_keys():
    """Get API keys from Streamlit secrets or environment variables."""
    import os.path
    secrets_paths = [
        os.path.expanduser("~/.streamlit/secrets.toml"),
        ".streamlit/secrets.toml"
    ]
    secrets_exist = any(os.path.exists(path) for path in secrets_paths)
    
    if secrets_exist:
        try:
            GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
        except KeyError:
            st.error("API keys not found in Streamlit secrets.")
            st.stop()
    else:
        # Fallback to environment variables for local development
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
        if not GEMINI_API_KEY:
            st.error("Missing API keys. For local development, create a .env file with GEMINI_API_KEY. For deployment, set them in Streamlit secrets.")
            st.stop()
    return GEMINI_API_KEY


GEMINI_API_KEY = get_api_keys()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3-flash-preview")

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return "user_role"

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])  # Initialize chat session
    
st.title("Geminie ChatBot 🤖")

for msg in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(msg.role)):
        st.markdown(msg.parts[0].text)
        
user_prompt = st.chat_input("Type your question here...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)