import streamlit as st
import json
import requests
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    st.title("LangFlow API Interface")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    application_token = st.sidebar.text_input(
        "Application Token",
        value=os.environ.get("APPLICATION_TOKEN", ""),
        type="password"
    )
    
    endpoint = st.sidebar.text_input(
        "Endpoint",
        value=FLOW_ID,
        help="Enter the flow ID or endpoint name"
    )
    
    # Advanced settings expander
    with st.sidebar.expander("Advanced Settings"):
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
        
        # Tweaks editor
        tweaks_str = st.text_area(
            "Tweaks (JSON)",
            value=json.dumps(DEFAULT_TWEAKS, indent=2),
            height=300
        )
        try:
            tweaks = json.loads(tweaks_str)
        except json.JSONDecodeError:
            st.error("Invalid JSON in tweaks")
            tweaks = DEFAULT_TWEAKS

    # Main chat interface
    st.header("Chat Interface")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Enter your message"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get response from API
        with st.spinner("Thinking..."):
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
                with st.expander("View Raw Response"):
                    st.json(response)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.error("Please check your configuration and try again.")

if __name__ == "__main__":
    main()