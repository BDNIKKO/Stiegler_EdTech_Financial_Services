from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pickle
import numpy as np
import os
import time
from sqlalchemy.exc import OperationalError

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# PostgreSQL configuration
POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'admin')  # Ensure consistency

app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql://admin:admin@postgres:5432/admin"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"Connecting to: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize database connection
db = SQLAlchemy(app)

# Retry mechanism to ensure database is ready
def wait_for_db():
    while True:
        try:
            db.session.execute('SELECT 1')
            print("Database is ready!")
            break
        except OperationalError:
            print("Database not ready, retrying in 5 seconds...")
            time.sleep(5)

# Loan Application model
class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_income = db.Column(db.Float, nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    credit_history = db.Column(db.Integer, nullable=False)
    debt_to_income = db.Column(db.Float, nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)
    employment_length = db.Column(db.Integer, nullable=False)
    loan_to_income = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.String(10), nullable=False)
    probability = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# Load the logistic regression model and scaler from Pickle
with open('models/logistic_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Handle loan predictions and save to the database."""
    try:
        # Get input data from the request
        data = request.json

        # Prepare feature set for the model
        features = np.array([[
            data['income'],
            data['loan_amount'],
            data['credit_history'],
            data['debt_to_income'],
            data['loan_term'],
            data['employment_length'],
            data['loan_to_income']
        ]])

        # Scale the features
        scaled_features = scaler.transform(features)

        # Make prediction
        prediction = model.predict(scaled_features)[0]
        probability = model.predict_proba(scaled_features)[0][1]
        result = 'Approved' if prediction == 1 else 'Denied'

        # Save result to database
        new_application = LoanApplication(
            applicant_income=data['income'],
            loan_amount=data['loan_amount'],
            credit_history=data['credit_history'],
            debt_to_income=data['debt_to_income'],
            loan_term=data['loan_term'],
            employment_length=data['employment_length'],
            loan_to_income=data['loan_to_income'],
            prediction=result,
            probability=probability
        )
        db.session.add(new_application)
        db.session.commit()

        return jsonify({'prediction': result, 'probability': probability})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        wait_for_db()  # Ensure database is ready before creating tables
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5000, debug=True)
