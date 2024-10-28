# Import necessary modules
import pickle
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as np
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

# Loan model to store loan application details and decision
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    income = db.Column(db.Float, nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)
    employment_length = db.Column(db.Float, nullable=False)
    decision = db.Column(db.String(10), nullable=False)  # 'Approved' or 'Denied'
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# User model definition
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Load the trained logistic regression model and scaler
with open('models/logistic_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get token from headers
        token = request.headers.get('Authorization')

        # If no token is provided, check if the admin bypass is applicable
        if not token:
            logging.debug("No token provided, checking if admin user is bypassed.")

            # Bypass token validation if admin is accessing the route
            auth_username = request.json.get('username', None)
            if auth_username == 'admin':
                logging.debug("Bypassing authentication for admin user.")
                return f(*args, **kwargs)

            # If it's not the admin, deny access
            return jsonify({'message': 'Token is missing!'}), 401

        # If a token exists, extract it from "Bearer <token>"
        if token.startswith("Bearer "):
            token = token.split("Bearer ")[1]

        try:
            # Decode the JWT token to get the username
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            username = data.get('user')

            # If the decoded user is admin, bypass further checks
            if username == 'admin':
                logging.debug("Admin user detected, bypassing further token validation.")
                return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        # Proceed to the route if everything is valid
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

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists. Please choose a different one.'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        logging.error(f"Error occurred while registering user: {e}")
        return jsonify({'message': 'Registration failed due to server error. Please try again.'}), 500

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
        # Bypass password verification for admin user
        if username == 'admin':
            logging.info("Bypassing password check for admin user.")
        elif not check_password_hash(user.password, password):
            logging.error(f"Invalid password for user '{username}'.")
            return jsonify({'message': 'Invalid credentials!'}), 401
    except Exception as e:
        logging.exception(f"Error during password verification: {e}")
        return jsonify({'message': 'Internal server error.'}), 500

    # Issue JWT token on successful login
    token = jwt.encode(
        {'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)},
        app.config['SECRET_KEY'], algorithm="HS256"
    )
    logging.debug(f"Issued Token: {token}")
    return jsonify({'token': token})

@token_required
def predict():
    data = request.get_json()
    features = [data.get('income'), data.get('loan_amount'), data.get('loan_term'), data.get('employment_length')]

    if None in features:
        return jsonify({'message': 'Missing required input values!'}), 400

    try:
        features = list(map(float, features))
    except ValueError:
        return jsonify({'message': 'All input values must be numbers!'}), 400

    income, loan_amount, loan_term, employment_length = features
    loan_term_months = loan_term * 12
    debt_to_income = (loan_amount / income) * 100
    loan_to_income = (loan_amount / income) * 100
    credit_history = 1 if employment_length > 5 else 0

    features = [income, loan_amount, loan_term_months, employment_length, debt_to_income, loan_to_income, credit_history]
    features = np.array(features).reshape(1, -1)
    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)

    if debt_to_income > 40 or income < 20000:
        result = 'Denied'
    else:
        result = 'Approved' if prediction[0] == 1 else 'Denied'

    # Log loan details in the database
    loan_entry = Loan(
        income=income,
        loan_amount=loan_amount,
        loan_term=loan_term,
        employment_length=employment_length,
        decision=result
    )
    db.session.add(loan_entry)
    db.session.commit()

    return jsonify({'prediction': result})

if __name__ == '__main__':
    db.create_all()  # Ensure tables are created
    app.run(debug=True, host='0.0.0.0', port=5000)
