import pickle
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
import numpy as np
import os

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# PostgreSQL configuration
POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'admin')

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:admin@postgres:5432/admin"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database connection
db = SQLAlchemy(app)

# Load the trained logistic regression model and scaler
with open('models/logistic_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Extract input values from the JSON data
    income = float(data['income'])
    loan_amount = float(data['loan_amount'])
    loan_term_years = float(data['loan_term'])  # Input in years
    employment_length = float(data['employment_length'])

    # Convert loan term from years to months
    loan_term_months = loan_term_years * 12

    # Automatically calculate Debt-to-Income ratio (DTI)
    debt_to_income = (loan_amount / income) * 100

    # Automatically calculate Loan-to-Income ratio (LTI)
    loan_to_income = (loan_amount / income) * 100

    # Automatically calculate credit history based on employment length
    credit_history = 1 if employment_length > 5 else 0  # Good credit if employment > 5 years

    # Prepare the feature array for prediction
    input_features = np.array([[income, loan_amount, loan_term_months, employment_length, debt_to_income, loan_to_income, credit_history]])

    # Log input features for debugging
    print("Input features used for prediction:", input_features)

    # Scale the input
    scaled_input = scaler.transform(input_features)

    # Get the initial prediction from the model
    prediction = model.predict(scaled_input)[0]

    # Apply additional business logic for more realistic results
    result = 'Approved' if prediction == 1 else 'Denied'
    
    # Custom rule-based adjustments for more realistic decisions
    if debt_to_income > 36:
        result = 'Denied'  # High debt-to-income ratio
    elif loan_to_income > 40:
        result = 'Denied'  # High loan-to-income ratio
    elif income < 30000 and credit_history == 0:
        result = 'Denied'  # Low income with bad credit history
    elif employment_length < 2 and income < 50000:
        result = 'Denied'  # Short employment and low income

    # Log the final decision for debugging
    print("Final Prediction Result (after rules):", result)

    # Return the prediction result as 'Approved' or 'Denied'
    return jsonify({'prediction': result})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5000, debug=True)
