import json
import requests
import uuid
from typing import Optional
from .config import BASE_API_URL, FLOW_ID, ENDPOINT_ID, API_HEADERS

def parse_error_message(error_response):
    """Parse error response and return a user-friendly message."""
    try:
        # Get the detail string
        detail = error_response.get("detail", "{}")
        
        # If detail is already a dictionary, use it directly
        if isinstance(detail, dict):
            error_detail = detail
        else:
            # Try to parse the JSON string
            error_detail = json.loads(detail)
        
        # Extract the message from the nested structure
        error_message = error_detail.get("message", "")
        
        # Common error patterns and their user-friendly messages
        error_patterns = {
            "429 Resource has been exhausted": "API quota has been exceeded. Please try again later.",
            "Error building Component Google Generative AI": "There was an issue with the AI model. Please try again later.",
            "Invalid token": "Invalid API token. Please check your configuration.",
            "Connection refused": "Unable to connect to the server. Please check your internet connection.",
        }
        
        # Check if any known error pattern matches
        for pattern, friendly_message in error_patterns.items():
            if pattern in error_message:
                return friendly_message
        
        # If no specific pattern matches, return the cleaned error message
        return error_message or "An unknown error occurred. Please try again."
    except Exception as e:
        # If parsing fails, return a generic message
        return "An error occurred while processing your request. Please try again."

def run_flow(
    message: str,
    endpoint: str = ENDPOINT_ID,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    session_id: Optional[str] = None
) -> dict:
    """Run a flow with a given message using the new Langflow API structure."""
    api_url = f"{BASE_API_URL}/lf/{FLOW_ID}/api/v1/run/{endpoint}"
    
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
        "session_id": session_id or str(uuid.uuid4())
    }
    
    if tweaks:
        payload["tweaks"] = tweaks
    
    response = requests.post(api_url, json=payload, headers=API_HEADERS)
    return response.json()