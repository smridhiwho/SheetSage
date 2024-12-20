from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope of the access needed
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate using the service account
creds = ServiceAccountCredentials.from_json_keyfile_name('your_key.json', scope)
client = gspread.authorize(creds)

# Build the service for Google Sheets API
service = build('sheets', 'v4', credentials=creds)

# Open the Google Spreadsheet by its name
spreadsheet = client.open_by_key("#########")

from transformers.agents import HfApiEngine

def generate_code_prompt(command, spreadsheet_id):
    model = "Qwen/Qwen2.5-72B-Instruct"
    llm_engine = HfApiEngine(model)  # Initialize the LLM engine

    # Prepare the prompt as a message dictionary with 'role' and 'content'
    prompt = [
        {
            "role": "system",
            "content": """You are an assistant that generates Python code to prepare request payloads for the Google Sheets API.
                          However, some parts of the code, like the credentials loading, will be handled externally.
                          Do not include the credentials loading, or any other pre-existing setup. Focus only on the logic for interacting with the Google Sheets API."""
        },
        {
            "role": "user",
            "content": f"The spreadsheet ID is {spreadsheet_id}. Generate Python code to create a proper request payload for the following task: {command}."
        }
    ]

    # Use the LLM engine to generate the response (code)
    response = llm_engine(messages=prompt)  # Pass the prompt as a list of dictionaries

    # Debugging: Print the response to check its structure
    print("Response:", response)

    return response

import json
from google.oauth2.credentials import Credentials

def process_generated_code(response, spreadsheet_id):
    # Check if the response is a string or list, and return the appropriate value
    if isinstance(response, list) and len(response) > 0:
        generated_code = response[0].get('generated_text', "No generated text found.")
    elif isinstance(response, str):
        generated_code = response
    else:
        generated_code = "Unexpected response format."

    # Extract the code block between the backticks
    start_marker = "```python"
    end_marker = "```"

    start_index = generated_code.find(start_marker)
    end_index = generated_code.find(end_marker, start_index + len(start_marker))

    if start_index != -1 and end_index != -1:
        code_to_execute = generated_code[start_index + len(start_marker):end_index].strip()
    else:
        code_to_execute = "No valid code block found between backticks."

    # Full Python code with external setup
    full_code = f"""
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# External setup (credentials)
SPREADSHEET_ID = '{spreadsheet_id}'

from google.oauth2.service_account import Credentials
import json

# Assuming you have the content of your JSON credentials as a string or dictionary
json_content = '''
{{
  "type": "service_account",
  "project_id": "#########",
  "private_key_id": "your_private_Key_id",
  "private_key": "-----BEGIN PRIVATE KEY-----\\<private key>\\n-----END PRIVATE KEY-----\\n",
  "client_email": "####@#########.iam.gserviceaccount.com",
  "client_id": "102847724607841703990",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/####%40#########.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}}

# Convert the string content into a Python dictionary
credentials_info = json.loads(json_content)

# Use from_json_keyfile_dict instead of from_json_keyfile_name
creds = Credentials.from_service_account_info(credentials_info)

# Build the Google Sheets API service
service = build('sheets', 'v4', credentials=creds)

# Extracted code block to be executed
{code_to_execute}
"""

    # Return the full code block with external setup included
    return full_code

def execute_code(full_code, service, spreadsheet_id):
    try:
      exec(full_code, globals())

      # Assuming the generated code sets up a 'chart' variable as the payload
      response = service.spreadsheets().batchUpdate(
          spreadsheetId=spreadsheet_id
      ).execute()
      print(f"Response: {response}")


    except Exception as e:
        print(f"Error executing the code: {e}")


def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('your_key.json', scope)
    client = gspread.authorize(creds)
    return client

@app.route('/log_spreadsheet_id', methods=['POST'])
def log_spreadsheet_id():
    data = request.get_json()
    spreadsheet_link = data.get('spreadsheetLink')
    prompt_input = data.get('promptExcel')  # Retrieve the prompt input
    client = authenticate_google_sheets()
    response = generate_code_prompt(user_command, spreadsheet_id)
    full_code = process_generated_code(response, spreadsheet_id)
    execute_code(full_code, client,spreadsheet_id)


    if not spreadsheet_link:
        return jsonify({"error": "Spreadsheet link is required"}), 400

    try:
        # Extract the spreadsheet ID from the link
        spreadsheet_id = spreadsheet_link.split("/d/")[1].split("/")[0]
        print(f"Spreadsheet ID: {spreadsheet_id}")  # Log the ID to the console
        print(f"Prompt Input: {prompt_input}")  # Log the prompt input to the console
        return jsonify({"message": "Data logged", "spreadsheetId": spreadsheet_id, "promptInput": prompt_input})
    except IndexError:
        return jsonify({"error": "Invalid spreadsheet link format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
