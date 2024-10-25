from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pickle
import pandas as pd  # Ensure consistent DataFrame handling
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
POSTGRES_DB = os.getenv('POSTGRES_DB', 'admin')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:admin@postgres:5432/admin"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"Connecting to: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize the database connection
db = SQLAlchemy(app)

# Load the trained logistic regression model and scaler
with open('models/logistic_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# The expected feature names, in the correct order
FEATURE_NAMES = [
    'income', 'loan_amount', 'credit_history',
    'debt_to_income', 'loan_term', 'employment_length', 'loan_to_income'
]

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Extract input values from the JSON data
    income = float(data['income'])
    loan_amount = float(data['loan_amount'])
    loan_term_years = float(data['loan_term'])
    employment_length = float(data['employment_length'])

    # Convert loan term from years to months
    loan_term_months = loan_term_years * 12

    # Calculate derived features
    debt_to_income = (loan_amount / income) * 100
    loan_to_income = (loan_amount / income) * 100
    credit_history = 1 if employment_length > 5 else 0

    # Create a DataFrame with the same feature names and order as used during training
    input_data = pd.DataFrame([[
        income, loan_amount, credit_history, debt_to_income,
        loan_term_months, employment_length, loan_to_income
    ]], columns=FEATURE_NAMES)

    # Log the input data for debugging
    print("Input data for prediction:", input_data)

    # Scale the input data
    scaled_input = scaler.transform(input_data)

    # Make a prediction
    prediction = model.predict(scaled_input)[0]

    # Log the prediction result
    print("Prediction result:", prediction)

    # Return the result as 'Approved' or 'Denied'
    result = 'Approved' if prediction == 1 else 'Denied'
    return jsonify({'prediction': result})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5000, debug=True)
