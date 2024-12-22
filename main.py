# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token

import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

import os
from dotenv import load_dotenv
load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "6cb8d6b9-cc9a-4abc-92a9-aa41bf5d93eb"
FLOW_ID = "4fb7c099-22dd-43d9-b9ec-0a403a68f9e3"
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "ChatInput-HdACw": {
    # "background_color": "",
    # "chat_icon": "",
    # "files": "",
    # "input_value": "जीवा उवाओगामाओ, अमुत्ती कट्टा सदेहपरिमानो। भोत्ता संसारत्थो, सिद्धो सो विस्सोडन्कगै ॥2॥\n\nभावार्थ बताइए ",
    # "sender": "User",
    # "sender_name": "User",
    # "session_id": "",
    # "should_store_message": True,
    # "text_color": ""
  },
  "ChatOutput-dzZWQ": {
    # "background_color": "",
    # "chat_icon": "",
    # "data_template": "{text}",
    # "input_value": "",
    # "sender": "Machine",
    # "sender_name": "AI",
    # "session_id": "",
    # "should_store_message": True,
    # "text_color": ""
  },
  "ParseData-PSHqh": {
    # "sep": "\n",
    # "template": "{text}"
  },
  "File-6yiwZ": {
    # "concurrency_multithreading": 4,
    # "path": "Dravyasangrah.pdf",
    # "silent_errors": False,
    # "use_multithreading": False
  },
  "Prompt-BONxv": {
    # "Document": "",
    # "template": "Answer user's questions based on the document below:\n\n---\n\n{Document}\n\n---\n\nQuestion:"
  },
  "GoogleGenerativeAIModel-nVd6m": {
    # "google_api_key": "AIzaSyA8zhYBca7b-11l3KEyfzzhMjGEj_SHvos",
    # "input_value": "",
    # "max_output_tokens": None,
    # "model": "gemini-1.5-pro",
    # "n": None,
    # "stream": False,
    # "system_message": "",
    # "temperature": 0.1,
    # "top_k": None,
    # "top_p": None
  }
}

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
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
    parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument("message", type=str, help="The message to send to the flow")
    parser.add_argument("--endpoint", type=str, default=ENDPOINT or FLOW_ID, help="The ID or the endpoint name of the flow")
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
