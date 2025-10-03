# Gender Classifier App

A full-stack application that predicts gender based on physical characteristics.

## Tech Stack
- **Frontend**: React 19.1.1
- **Backend**: Flask (Python)
- **Database**: SQLite

## Setup
To properly run the application, you need to install the dependencies for both the frontend and backend

Run both the frontend and backend using the commands below

Once you got it running, run backend/populate_db.py to populate the database
You can verify a populated database with backend/PersonDatabaseViewer.py

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```