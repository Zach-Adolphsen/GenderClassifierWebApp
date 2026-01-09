from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sklearn import neighbors
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgresql://'):
    # Fix the PostgreSQL URL scheme for SQLAlchemy
    database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'person_data'
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    shoe_size = db.Column(db.Float)
    gender = db.Column(db.String(6))

    def to_dict(self):
        return {
            'id': self.id,
            'height': self.height,
            'weight': self.weight,
            'shoe_size': self.shoe_size,
            'gender': self.gender,
        }

@app.get("/")
def health():
    return {"status": "ok"}

@app.route('/api/predict', methods=['POST'])
def predict_gender():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        height = float(data.get('height', 0))
        weight = float(data.get('weight'))
        shoe_size = float(data.get('shoeSize'))
        print(f"Received data: height={height}, weight={weight}, shoe_size={shoe_size}")

        confidence, prediction = gender_classifier(height, weight, shoe_size)
        return jsonify({
            'confidence': float(confidence),
            'prediction': prediction,
        })
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred during prediction'}), 500


def gender_classifier(height, weight, shoe_size):
    predictions = []
    probabilities = []

    try:
        X, Y = get_training_data()
    except Exception as e:
        raise e

    newUserDetails = [[height, weight, shoe_size]]

    # K Neighbors
    clf = neighbors.KNeighborsClassifier().fit(X, Y)
    pred = clf.predict(newUserDetails)
    predictions.append(pred[0])
    prob = clf.predict_proba(newUserDetails)
    probabilities.append(prob)

    # Quadratic Discriminant Analysis
    clf = QuadraticDiscriminantAnalysis().fit(X, Y)
    pred = clf.predict(newUserDetails)
    predictions.append(pred[0])
    prob = clf.predict_proba(newUserDetails)
    probabilities.append(prob)

    # Random Forest
    clf = RandomForestClassifier().fit(X, Y)
    pred = clf.predict(newUserDetails)
    predictions.append(pred[0])
    prob = clf.predict_proba(newUserDetails)
    probabilities.append(prob)

    best_algo_index = 0
    best_confidence = 0
    for i, prob in enumerate(probabilities):
        if prob.max() > best_confidence:
            best_confidence = prob.max()
            best_algo_index = i

    return float(best_confidence), predictions[best_algo_index]


def get_training_data():
    try:
        persons = Person.query.all()

        if not persons or len(persons) == 0:
            raise ValueError("No training data found")

        details = []
        genders = []

        for person in persons:
            details.append([float(person.height), float(person.weight), float(person.shoe_size)])
            genders.append(person.gender)

        return details, genders
    except Exception as e:
        print(f"Database Error: {str(e)}")
        raise e


@app.route('/api/add-person', methods=['POST'])
def add_user():
    data = request.get_json()
    print(f"Received data: {data}")

    new_user = Person(height=data.get('height'),
                      weight=data.get('weight'),
                      shoe_size=data.get('shoeSize'),
                      gender=data.get('gender'))

    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
