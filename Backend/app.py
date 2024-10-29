# Import necessary modules
import pickle
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
import os
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import logging

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app, 
     resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:8080"]}},
     supports_credentials=True)

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

# Loan model to store loan application details and decision
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    income = db.Column(db.Float, nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)
    employment_length = db.Column(db.Float, nullable=False)
    decision = db.Column(db.String(10), nullable=False)  # 'Approved' or 'Denied'
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

# User model definition
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)

# Load the trained logistic regression model and scaler
with open('models/logistic_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        logging.info(f"Received token in decorator: {token}")

        if not token:
            logging.error("Token is missing")
            return jsonify({'message': 'Token is missing!'}), 401

        if token.startswith("Bearer "):
            token = token.split("Bearer ")[1]

        try:
            # Decode the JWT token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            logging.info(f"Decoded token data: {data}")
            
            # Check if user is admin
            if data.get('user') != 'admin':
                logging.error("Non-admin user attempted to access analytics")
                return jsonify({'message': 'Admin access required'}), 403
                
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired")
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError as e:
            logging.error(f"Invalid token: {str(e)}")
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)
    return decorated

# User registration route
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('address')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists.'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(
        username=username, password=hashed_password, 
        first_name=first_name, last_name=last_name, 
        phone=phone, email=email, address=address
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        logging.error(f"Error occurred while registering user: {e}")
        return jsonify({'message': 'Registration failed due to server error.'}), 500

# User login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        logging.error(f"User '{username}' not found.")
        return jsonify({'message': 'Invalid credentials!'}), 401

    try:
        # Bypass password check for admin user
        if username == 'admin':
            logging.info("Bypassing password check for admin user.")
        elif not check_password_hash(user.password, password):
            logging.error(f"Invalid password for user '{username}'.")
            return jsonify({'message': 'Invalid credentials!'}), 401
    except Exception as e:
        logging.exception(f"Error during password verification: {e}")
        return jsonify({'message': 'Internal server error.'}), 500

    # Issue JWT token for both admin and regular users
    token = jwt.encode(
        {'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)},
        app.config['SECRET_KEY'], algorithm="HS256"
    )
    logging.debug(f"Issued Token: {token}")
    return jsonify({'token': token})

@app.route('/api/predict', methods=['POST'])  # Add this decorator
@token_required
def predict():
    logging.info("Predict route accessed.")

    # Extract the username from the JWT token
    token = request.headers.get('Authorization')
    if token and token.startswith("Bearer "):
        token = token.split("Bearer ")[1]
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token.get('user')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        logging.error(f"Token error: {e}")
        return jsonify({'message': 'Invalid or expired token!'}), 401

    # Fetch the user from the database
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    # Extract features from request
    data = request.get_json()
    features = [
        data.get('income'),
        data.get('loan_amount'),
        data.get('loan_term'),
        data.get('employment_length')
    ]

    if None in features:
        return jsonify({'message': 'Missing required input values!'}), 400

    try:
        features = list(map(float, features))
    except ValueError:
        return jsonify({'message': 'All input values must be numbers!'}), 400

    # MLM Logic: Calculate additional features
    income, loan_amount, loan_term, employment_length = features
    loan_term_months = loan_term * 12
    debt_to_income = (loan_amount / income) * 100
    loan_to_income = (loan_amount / income) * 100
    credit_history = 1 if employment_length > 5 else 0

    # Prepare feature set for model prediction
    features = [
        income, loan_amount, loan_term_months,
        employment_length, debt_to_income,
        loan_to_income, credit_history
    ]
    features = np.array(features).reshape(1, -1)

    with np.errstate(all='ignore'):
        features_scaled = scaler.transform(features)

    # Get prediction from the model
    prediction = model.predict(features_scaled)

    # Apply business rules for final decision
    if debt_to_income > 40 or income < 20000:
        result = 'Denied'
    else:
        result = 'Approved' if prediction[0] == 1 else 'Denied'

    # Log loan details along with user information
    loan_entry = Loan(
        income=income,
        loan_amount=loan_amount,
        loan_term=loan_term,
        employment_length=employment_length,
        decision=result,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        email=user.email
    )
    db.session.add(loan_entry)
    db.session.commit()

    return jsonify({'prediction': result})

@app.route('/api/loan-analytics', methods=['GET'])
@token_required
def get_loan_analytics():
    try:
        logging.info("Accessing loan analytics endpoint")
        
        # Get token from request
        token = request.headers.get('Authorization')
        logging.info(f"Received token: {token}")

        # Query the database
        analytics = db.session.execute("SELECT * FROM loan_analytics ORDER BY last_updated DESC LIMIT 1").fetchone()
        logging.info(f"Query result: {analytics}")
        
        if not analytics:
            logging.warning("No analytics data found")
            return jsonify({'message': 'No analytics data available'}), 404

        result = {
            'total_applications': analytics.total_applications,
            'approved_count': analytics.approved_count,
            'denied_count': analytics.denied_count,
            'approval_rate': analytics.approval_rate,
            'avg_loan_amount': analytics.avg_loan_amount,
            'last_updated': str(analytics.last_updated),  # Convert to string
        }
        logging.info(f"Returning result: {result}")
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error in get_loan_analytics: {str(e)}")
        return jsonify({'message': f'Error: {str(e)}'}), 500
