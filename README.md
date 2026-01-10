# Gender Classifier Web Application

A full-stack web application that predicts a user’s gender based on biometric inputs using an ensemble of machine learning models. The application features a React frontend, a Flask REST API backend, and a PostgreSQL database for persistent training data.

---

## 🚀 Features

- Full-stack architecture using **React, Flask, and PostgreSQL**
- Machine learning **ensemble approach** with multiple classifiers:
  - K-Nearest Neighbors (KNN)
  - Quadratic Discriminant Analysis (QDA)
  - Random Forest
- **Confidence-based prediction selection** across models
- RESTful API for predictions and data ingestion
- Dynamic model training from database-stored user data
- User feedback loop to improve future predictions
- Cloud-ready backend configuration
- Interactive UI with built-in unit conversion guides

---

## 🧠 How It Works

1. Users input:
   - Height (cm)
   - Weight (kg)
   - Shoe size (EU)
2. The React frontend sends the data to the Flask API.
3. The backend:
   - Retrieves labeled training data from PostgreSQL
   - Trains multiple machine learning models
   - Generates predictions and confidence scores
   - Selects the prediction with the **highest confidence**
4. Results are returned to the frontend and displayed to the user.
5. Users can optionally submit feedback to improve future predictions.

---

## 🏗️ Tech Stack

### Frontend
- React
- JavaScript (ES6+)
- CSS
- Fetch API

### Backend
- Python
- Flask
- Flask-CORS
- SQLAlchemy
- scikit-learn

### Database
- PostgreSQL

### Machine Learning
- K-Nearest Neighbors
- Quadratic Discriminant Analysis
- Random Forest Classifier

---

## 📂 Project Structure

```text
GenderClassifierWebApp/
├── api/
│   └── index.py          # Flask backend and ML logic
├── frontend/
│   ├── src/
│   │   ├── App.js        # Main React application
│   │   ├── App.css
│   │   └── assets/       # Conversion images
│   └── package.json
├── README.md