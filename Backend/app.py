import pickle
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import logging

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Authorization", "Content-Type"])

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# PostgreSQL configuration
POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'admin')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8e8255b84da012f7e0fe37404dde07a0a2748ca7e9ee5c7f10d98daa168f029b'

# Initialize the database connection
db = SQLAlchemy(app)

# Load the trained logistic regression model and scaler
with open('models/logistic_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Decorator for token-required routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Remove 'Bearer ' prefix if present
        if token.startswith("Bearer "):
            token = token.split("Bearer ")[1]

        try:
            logging.debug(f"Attempting to decode token: {token}")
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired.")
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            logging.error("Token is invalid.")
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated

# User registration route
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    # Code to add user to database (not shown here)
    
    return jsonify({'message': 'User registered successfully!'}), 201

# User login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    # Code to verify user from the database (not shown here)
    
    # Assuming user is verified
    if True:  # Replace with actual check
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)}, app.config['SECRET_KEY'], algorithm="HS256")
        logging.debug(f"Issued Token: {token}")
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401

# Prediction endpoint
@app.route('/api/predict', methods=['POST'])
@token_required
def predict():
    data = request.get_json()
    features = [data.get('income'), data.get('loan_amount'), data.get('loan_term'), data.get('employment_length')]

    if None in features:
        return jsonify({'message': 'Missing required input values!'}), 400

    # Validate that all inputs are numeric
    try:
        features = list(map(float, features))
    except ValueError:
        return jsonify({'message': 'All input values must be numbers!'}), 400

    # Calculate additional features
    income, loan_amount, loan_term, employment_length = features
    loan_term_months = loan_term * 12
    debt_to_income = (loan_amount / income) * 100
    loan_to_income = (loan_amount / income) * 100
    credit_history = 1 if employment_length > 5 else 0

    # Update features to include calculated fields
    features = [income, loan_amount, loan_term_months, employment_length, debt_to_income, loan_to_income, credit_history]

    features = np.array(features).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)

    result = 'Approved' if prediction[0] == 1 else 'Denied'
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
