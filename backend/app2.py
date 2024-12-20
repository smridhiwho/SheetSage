from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/log_spreadsheet_id', methods=['POST'])
def log_spreadsheet_id():
    data = request.get_json()
    spreadsheet_link = data.get('spreadsheetLink')
    prompt_input = data.get('promptExcel')  # Retrieve the prompt input

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
