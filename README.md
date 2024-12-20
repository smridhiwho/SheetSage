# SheetSage

SheetSage is a React-based, multi-agentic web application designed to simplify interactions
with Google Sheets. It leverages Large Language Models (LLMs) to convert layman user
queries into actionable spreadsheet operations, eliminating the need for complex Excel
formulas or Google Sheets scripting knowledge. SheetSage empowers users by providing
an intuitive interface to execute advanced spreadsheet tasks with ease.

## Features

- Provide prompts for tasks related to the spreadsheet.
- Maintain a history of embedded spreadsheets with options to rename or delete.
- History is persisted in the browser's local storage.
- Stylish and responsive UI with gradient backgrounds and icons.

## Technologies Used

### Frontend

- *React*: For building the user interface.
- *TailwindCSS*: For styling.
- *React Icons*: For the icons used in the application.

### Backend

- *Flask*: For handling API requests.
- *Flask-CORS*: To manage cross-origin requests.
---

## Architecture

![architecture](https://github.com/user-attachments/assets/5a4d6f3d-be44-411f-bfc7-0a9d4cc0fefe)

---

### Demo Video

To see a demonstration of the application in action, check out the [demo video](https://youtu.be/PEG-G3RJuaw).

---

## Getting Started

Follow these steps to set up and run the project locally:


## Project Structure

- `backend/`
  - `venv/`: Virtual environment for the backend.
  - `app.py`: Main Flask application with Google Sheets API logic and LLM prompt generation.
  - `app2.py`: Simplified version of the Flask app.
  
- `frontend/`: Basic React app to collect user input for JSON key, Google Sheets link, and prompt.

### Prerequisites

- *Node.js*: [Download and install Node.js](https://nodejs.org/).
- *Python 3.x*: Ensure Python is installed on your system.
- *pip*: Python package manager (comes with Python).

---

### Frontend Setup

1. **Navigate to the frontend directory:**

   ```
   cd frontend
   ```

2. **Install dependencies:**

   ```
   npm install
   ```

3.**Run the development server:**

   ```
   npm run dev
   ```

4. Open your browser and visit:
   
   http://localhost:5173
   

---

### Backend Setup

1. **Navigate to the backend directory:**

   ```
   cd backend
   ```

2. **Create a virtual environment (optional but recommended):**

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install dependencies:**

  ```
   pip install flask flask-cors
```
```
   pip install gspread oauth2client matplotlib pandas transformers[agents] google-api-python-client -qU
```
4. **Add Google Cloud Credentials**
Copy your Google Cloud JSON key file to the backend/ directory.
Rename the key file to  `your_key.json` (or update the code if using a different file name).

### Google Sheets API Setup
Enable Google Sheets API:

Go to the Google Cloud Console([https://console.cloud.google.com/apis/api/drive.googleapis.com/overview?project=hackathon-445215&inv=1&invt=AbknyQ](https://console.cloud.google.com/).
- Create a new project (if you don't have one).
- Go to the API & Services Dashboard and enable the Google Sheets API.

Create a Service Account:
- Go to the "IAM & Admin" section and create a new service account.
- Generate a new key for the service account in JSON format.
5. **Run the Flask server:**

   ```
   python server.py
   ```

6. The backend will be running at:
   
   http://localhost:5000
   

---

### Troubleshooting

#### CORS Error

If you encounter a CORS error when trying to fetch from the backend, ensure the Flask server has Flask-CORS properly installed and configured:

```
from flask_cors import CORS
CORS(app)
```

#### Dependencies Issues

If a dependency is missing, run the following command in the appropriate directory:

- For frontend:
  ```
  npm install <package-name>
  ```
- For backend:
  ```
  pip install <package-name>
  ```

---

### Future Enhancements

- Add user authentication.
- Allow for sharing of spreadsheet history across devices.
- Integrate AI-based prompt suggestions.

---

### License

This project is licensed under the MIT License.



```





