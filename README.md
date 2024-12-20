# SheetSage

SheetSage is a React-based, multi-agentic web application designed to simplify interactions
with Google Sheets. It leverages Large Language Models (LLMs) to convert layman user
queries into actionable spreadsheet operations, eliminating the need for complex Excel
formulas or Google Sheets scripting knowledge. SheetSage empowers users by providing
an intuitive interface to execute advanced spreadsheet tasks with ease.

## Prerequisites

Before running the app, make sure you have the following installed on your machine:

- **Python 3.8+**
- **Node.js (for running the React frontend)**
- **Google Cloud JSON key**: You'll need a Google Cloud project with the Google Sheets API enabled.

## Project Structure

- `backend/`
  - `venv/`: Virtual environment for the backend.
  - `app.py`: Main Flask application with Google Sheets API logic and LLM prompt generation.
  - `app2.py`: Simplified version of the Flask app.
  
- `frontend/`: Basic React app to collect user input for JSON key, Google Sheets link, and prompt.

## Setting Up the Backend

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Set Up Python Virtual Environment**
   Create and activate a virtual environment:
   ```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Add Google Cloud Credentials**
Copy your Google Cloud JSON key file to the backend/ directory.
Rename the key file to  `your_key.json` (or update the code if using a different file name).

5. **Run the Flask App**
run `python app.py`
The backend will be running on http://127.0.0.1:5000/.

## Setting Up the Frontend

### Navigate to the Frontend Directory:
```
cd frontend
```
### Install Node.js Dependencies:
```
npm install
```

### Run the React App:
```
npm start
```

The React app will be running on http://localhost:3000/.




