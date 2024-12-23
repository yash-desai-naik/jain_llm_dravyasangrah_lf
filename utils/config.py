import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "6cb8d6b9-cc9a-4abc-92a9-aa41bf5d93eb"
FLOW_ID = "4fb7c099-22dd-43d9-b9ec-0a403a68f9e3"
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN", "")

# Default tweaks configuration
DEFAULT_TWEAKS = {
    "ChatInput-HdACw": {},
    "ChatOutput-dzZWQ": {},
    "ParseData-PSHqh": {},
    "File-6yiwZ": {
        # "path": "Dravyasangrah.txt",  # Default book
        # "concurrency_multithreading": 4,
        # "silent_errors": False,
        # "use_multithreading": False
    },
    "Prompt-BONxv": {},
    "GoogleGenerativeAIModel-nVd6m": {}
}

# Page configuration
PAGE_CONFIG = {
    "page_title": "Jain Texts AI QnA",
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
}