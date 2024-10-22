from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pickle
import numpy as np
import os

# Initialize Flask app and enable CORS to allow frontend communication
app = Flask(__name__)
CORS(app)

# PostgreSQL configuration from environment variables
POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'loan_db')

# Database URI for PostgreSQL (running in Docker container)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database connection
db = SQLAlchemy(app)

# Define Loan Application model for storing results in PostgreSQL
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
    probability = db.Column(db.Float, nullable=False)  # Store probability score
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# Load the logistic regression model and scaler from Pickle files
with open('models/logistic_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Handle loan prediction requests from the frontend."""
    try:
        # Get JSON data from the frontend
        data = request.json

        # Extract and format the input features
        features = np.array([[
            data['income'], 
            data['loan_amount'], 
            data['credit_history'],
            data['debt_to_income'],
            data['loan_term'], 
            data['employment_length'],
            data['loan_to_income']
        ]])

        # Scale the input features using the pre-fitted scaler
        scaled_features = scaler.transform(features)

        # Predict loan approval and calculate probability
        prediction = model.predict(scaled_features)[0]
        probability = model.predict_proba(scaled_features)[0][1]  # Probability of approval

        # Convert prediction to human-readable result
        result = 'Approved' if prediction == 1 else 'Denied'

        # Store the loan application result in PostgreSQL
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

        # Return the prediction and probability to the frontend
        return jsonify({'prediction': result, 'probability': probability})

    except Exception as e:
        # Handle errors and return a meaningful message to the frontend
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Ensure the database is created when the app starts
    with app.app_context():
        db.create_all()
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
