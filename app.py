import streamlit as st
import json
import requests
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config and SEO
st.set_page_config(
    page_title="Dravyasangrah Book AI QnA",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/dravyasangrah-ai',
        'Report a bug': "https://github.com/yourusername/dravyasangrah-ai/issues",
        'About': "# Dravyasangrah Book AI QnA\n\nAn AI-powered interface for exploring and understanding the Dravyasangrah text."
    }
)

# Add custom CSS
st.markdown("""
    <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .main-header {
            text-align: center;
            color: #1E3C72;
            margin-bottom: 2rem;
        }
        .description {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        .chat-container {
            border-radius: 10px;
            padding: 20px;
            background-color: #f8f9fa;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Constants from original script
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "6cb8d6b9-cc9a-4abc-92a9-aa41bf5d93eb"
FLOW_ID = "4fb7c099-22dd-43d9-b9ec-0a403a68f9e3"
DEFAULT_TWEAKS = {
    "ChatInput-HdACw": {},
    "ChatOutput-dzZWQ": {},
    "ParseData-PSHqh": {},
    "File-6yiwZ": {},
    "Prompt-BONxv": {},
    "GoogleGenerativeAIModel-nVd6m": {}
}

def run_flow(
    message: str,
    endpoint: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None
) -> dict:
    """Run a flow with a given message and optional tweaks."""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    # Main header with custom styling
    st.markdown('<h1 class="main-header">📚 Dravyasangrah Book AI QnA</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="description">Ask questions about the Dravyasangrah text and get AI-powered answers. '
        'Explore the ancient wisdom with modern technology.</p>',
        unsafe_allow_html=True
    )
    
    # Sidebar configuration with improved organization
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/yourusername/dravyasangrah-ai/main/assets/logo.png", 
                use_container_width=True)
        st.header("⚙️ Configuration")
        
        # API Configuration section
        st.subheader("API Settings")
        application_token = st.text_input(
            "Application Token",
            value=os.environ.get("APPLICATION_TOKEN", ""),
            type="password",
            help="Enter your LangFlow API token"
        )
        
        endpoint = st.text_input(
            "Endpoint",
            value=FLOW_ID,
            help="Enter the flow ID or endpoint name"
        )
        
        # Advanced settings in organized sections
        with st.expander("🔧 Advanced Settings"):
            st.subheader("Response Format")
            output_type = st.selectbox(
                "Output Type",
                options=["chat", "text"],
                index=0
            )
            input_type = st.selectbox(
                "Input Type",
                options=["chat", "text"],
                index=0
            )
            
            st.subheader("Custom Tweaks")
            tweaks_str = st.text_area(
                "Tweaks (JSON)",
                value=json.dumps(DEFAULT_TWEAKS, indent=2),
                height=300,
                help="Customize the behavior of the AI model"
            )
            try:
                tweaks = json.loads(tweaks_str)
            except json.JSONDecodeError:
                st.error("Invalid JSON in tweaks")
                tweaks = DEFAULT_TWEAKS

    # Main chat interface with improved styling
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Welcome! I'm here to help you understand the Dravyasangrah text. Feel free to ask any questions about its teachings, concepts, or interpretations."
        })

    # Display chat history with improved styling
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input with error handling
    if prompt := st.chat_input("Ask your question about Dravyasangrah..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get response from API
        with st.spinner("Analyzing your question..."):
            try:
                response = run_flow(
                    message=prompt,
                    endpoint=endpoint,
                    output_type=output_type,
                    input_type=input_type,
                    tweaks=tweaks,
                    application_token=application_token
                )
                
                # Extract the response text
                response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

                # Show raw response in expander
                with st.expander("🔍 View Technical Details"):
                    st.json(response)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.error("Please check your configuration and try again.")

    st.markdown('</div>', unsafe_allow_html=True)

   

if __name__ == "__main__":
    main()