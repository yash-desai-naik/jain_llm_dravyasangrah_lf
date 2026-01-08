# Note: Updated for new Langflow API structure

import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
import uuid
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

import os
from dotenv import load_dotenv
load_dotenv()

BASE_API_URL = "https://aws-us-east-2.langflow.datastax.com"
FLOW_ID = "908641fd-b0ff-4754-9fce-230aea3ff378"
ENDPOINT_ID = "f098008e-9caa-4326-ac51-a4419a151537"
ORG_ID = "091af4c2-853c-4830-bf76-65583f31923a"
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")
ENDPOINT = ENDPOINT_ID  # Default endpoint

# You can tweak the flow by adding a tweaks dictionary
# e.g {"component_id": {"field": "value"}}
TWEAKS = {}

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks using the new Langflow API.

    :param message: The message to send to the flow
    :param endpoint: The endpoint ID of the flow
    :param tweaks: Optional tweaks to customize the flow
    :param application_token: Application token for authentication
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{FLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
        "session_id": str(uuid.uuid4())
    }
    headers = {
        "X-DataStax-Current-Org": ORG_ID,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers["Authorization"] = f"Bearer {application_token}"
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument("message", type=str, help="The message to send to the flow")
    parser.add_argument("--endpoint", type=str, default=ENDPOINT or ENDPOINT_ID, help="The endpoint ID of the flow")
    parser.add_argument("--tweaks", type=str, help="JSON string representing the tweaks to customize the flow", default=json.dumps(TWEAKS))
    parser.add_argument("--application_token", type=str, default=APPLICATION_TOKEN, help="Application Token for authentication")
    parser.add_argument("--output_type", type=str, default="chat", help="The output type")
    parser.add_argument("--input_type", type=str, default="chat", help="The input type")
    parser.add_argument("--upload_file", type=str, help="Path to the file to upload", default=None)
    parser.add_argument("--components", type=str, help="Components to upload the file to", default=None)

    args = parser.parse_args()
    try:
      tweaks = json.loads(args.tweaks)
    except json.JSONDecodeError:
      raise ValueError("Invalid tweaks JSON string")

    if args.upload_file:
        if not upload_file:
            raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
        elif not args.components:
            raise ValueError("You need to provide the components to upload the file to.")
        tweaks = upload_file(file_path=args.upload_file, host=BASE_API_URL, flow_id=ENDPOINT, components=args.components, tweaks=tweaks)

    response = run_flow(
        message=args.message,
        endpoint=args.endpoint,
        output_type=args.output_type,
        input_type=args.input_type,
        tweaks=tweaks,
        application_token=args.application_token
    )

    print(type(response))
    # write the response to a file
    with open("response.json", "w") as f:
        json.dump(response, f, indent=2)

    # print the anwser only
    print(response["outputs"][0]["outputs"][0]["results"]["message"]["text"])

if __name__ == "__main__":
    main()
