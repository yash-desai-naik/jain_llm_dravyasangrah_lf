import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Load credentials from token file
TOKEN_FILE = "yash.desai.naik@gmail.com-token.json"
try:
    with open(TOKEN_FILE, "r") as f:
        token_data = json.load(f)
    APPLICATION_TOKEN = token_data.get("token", os.environ.get("APPLICATION_TOKEN", ""))
    ORG_ID = token_data.get("orgId", "091af4c2-853c-4830-bf76-65583f31923a")
except (FileNotFoundError, json.JSONDecodeError):
    APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN", "")
    ORG_ID = os.environ.get("ORG_ID", "091af4c2-853c-4830-bf76-65583f31923a")

# API Configuration - Updated for new Langflow API
BASE_API_URL = "https://aws-us-east-2.langflow.datastax.com"
FLOW_ID = "908641fd-b0ff-4754-9fce-230aea3ff378"
ENDPOINT_ID = "f098008e-9caa-4326-ac51-a4419a151537"

# Default tweaks configuration (empty for new API structure)
DEFAULT_TWEAKS = {}

# Page configuration
PAGE_CONFIG = {
    "page_title": "Jain Texts AI QnA",
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
}

# API Headers for new Langflow format
API_HEADERS = {
    "X-DataStax-Current-Org": ORG_ID,
    "Authorization": f"Bearer {APPLICATION_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}