from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sklearn import neighbors
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
import os

app = Flask(__name__)
CORS(app)

database_url = os.environ.get("DATABASE_URL")

if database_url and database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg2://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)


class Person(db.Model):
    __tablename__ = "person_data"

    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    shoe_size = db.Column(db.Float)
    gender = db.Column(db.String(6))

    def to_dict(self):
        return {
            "id": self.id,
            "height": self.height,
            "weight": self.weight,
            "shoe_size": self.shoe_size,
            "gender": self.gender,
        }

@app.route("/")
def root():
    return jsonify({"status": "Flask API is live"})

@app.route("/api/predict", methods=["POST", "GET"])
def predict_gender():
    if request.method == "GET":
        return jsonify({"message": "You reached the endpoint with GET. The frontend should be using POST."})
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        height = float(data.get("height"))
        weight = float(data.get("weight"))
        shoe_size = float(data.get("shoeSize"))

        confidence, prediction = gender_classifier(height, weight, shoe_size)

        return jsonify({
            "confidence": float(confidence),
            "prediction": prediction
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/add-person", methods=["POST"])
def add_user():
    data = request.get_json()

    new_user = Person(
        height=data.get("height"),
        weight=data.get("weight"),
        shoe_size=data.get("shoeSize"),
        gender=data.get("gender")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

def gender_classifier(height, weight, shoe_size):
    X, Y = get_training_data()
    new_user = [[height, weight, shoe_size]]

    predictions = []
    probabilities = []

    # KNN
    clf = neighbors.KNeighborsClassifier().fit(X, Y)
    predictions.append(clf.predict(new_user)[0])
    probabilities.append(clf.predict_proba(new_user))

    # QDA
    clf = QuadraticDiscriminantAnalysis().fit(X, Y)
    predictions.append(clf.predict(new_user)[0])
    probabilities.append(clf.predict_proba(new_user))

    # Random Forest
    clf = RandomForestClassifier().fit(X, Y)
    predictions.append(clf.predict(new_user)[0])
    probabilities.append(clf.predict_proba(new_user))

    best_idx = max(range(len(probabilities)), key=lambda i: probabilities[i].max())
    return probabilities[best_idx].max(), predictions[best_idx]


def get_training_data():
    persons = Person.query.all()

    if not persons:
        raise ValueError("No training data found")

    details = []
    genders = []

    for person in persons:
        details.append([
            float(person.height),
            float(person.weight),
            float(person.shoe_size)
        ])
        genders.append(person.gender)

    return details, genders
