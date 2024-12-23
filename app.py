import streamlit as st
import time

from utils.config import PAGE_CONFIG, DEFAULT_TWEAKS, FLOW_ID
from utils.styles import CUSTOM_CSS
from utils.api import run_flow, parse_error_message

def init_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'tweaks' not in st.session_state:
        st.session_state.tweaks = DEFAULT_TWEAKS.copy()

def display_chat_history():
    """Display all messages in the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("is_error", False):
                st.markdown(f'<p style="color: #ff4b4b;">{message["content"]}</p>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(message["content"])
            if "response_time" in message:
                st.markdown(f'<p class="response-time">Response time: {message["response_time"]:.2f}s</p>', 
                          unsafe_allow_html=True)

def handle_user_input(prompt: str):
    """Process user input and get AI response."""
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.spinner("विश्लेषण कर रहा हूं..."):
        try:
            start_time = time.time()
            response = run_flow(
                message=prompt,
                endpoint=FLOW_ID,
                tweaks=st.session_state.tweaks
            )
            end_time = time.time()
            response_time = end_time - start_time

            # Check if response contains an error
            if isinstance(response, dict) and "detail" in response:
                error_message = parse_error_message(response)
                st.error(f"🚨 {error_message}")
                with st.expander("🔍 View Error Details"):
                    st.json(response)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"_Error: {error_message}_",
                    "is_error": True,
                    "response_time": response_time
                })
                return

            # Extract and display the response
            response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            with st.chat_message("assistant"):
                st.markdown(response_text)
                st.markdown(f'<p class="response-time">Response time: {response_time:.2f}s</p>', 
                          unsafe_allow_html=True)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text,
                "response_time": response_time
            })

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.error("कृपया पुनः प्रयास करें।")

def main():
    # Set page configuration
    st.set_page_config(**PAGE_CONFIG)
    
    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()

    # Main header
    st.markdown('<h1 class="main-header">📚 Jain Texts AI QnA</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="description">Ask questions about Dravyasangrah and explore ancient Jain wisdom.</p>',
        unsafe_allow_html=True
    )

    # Main chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Initialize chat with welcome message
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "नमस्कार! मैं द्रव्यसंग्रह के बारे में आपकी जिज्ञासाओं का समाधान करने में सहायता कर सकता हूं। कृपया अपना प्रश्न पूछें।"
        })

    # Display chat history
    display_chat_history()

    # Handle user input
    if prompt := st.chat_input("अपना प्रश्न यहाँ पूछें..."):
        handle_user_input(prompt)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()