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
import requests
import base64
from sqlalchemy import func

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
            
            # Only check for admin access on analytics endpoints
            if request.endpoint == 'get_loan_analytics' and data.get('user') != 'admin':
                logging.error("Non-admin user attempted to access analytics")
                return jsonify({'message': 'Admin access required'}), 403
            
            # Get current user
            current_user = User.query.filter_by(username=data['user']).first()
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
                
            return f(current_user, *args, **kwargs)
                
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired")
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError as e:
            logging.error(f"Invalid token: {str(e)}")
            return jsonify({'message': 'Token is invalid!'}), 401

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

@app.route('/api/predict', methods=['POST'])
@token_required
def predict(current_user):
    logging.info("Predict route accessed.")
    try:
        # Extract features from request
        data = request.get_json()
        features = [
            float(data.get('annual_income', 0)),
            float(data.get('loan_amount', 0)),
            float(data.get('loan_term', 0)),
            float(data.get('employment_length', 0))
        ]
        
        if 0 in features:
            return jsonify({'message': 'Missing required input values!'}), 400
            
        # Extract individual features
        income, loan_amount, loan_term, employment_length = features
        
        # Calculate key metrics
        debt_to_income = (loan_amount / income) * 100
        loan_to_income = (loan_amount / income) * 100
        credit_history = min(employment_length / 10, 1.0)  # Scales from 0 to 1 over 10 years

        # Initialize approved as False
        approved = False
        
        # First check if it's a "definitely approve" case
        if (debt_to_income <= 15 and
            income >= 50000 and
            employment_length >= 5 and
            loan_amount <= income * 0.25):
            approved = True
        else:
            # MLM and standard criteria check
            features_array = [
                income, loan_amount, loan_term,
                employment_length, debt_to_income,
                loan_to_income, credit_history
            ]
            features_array = np.array(features_array).reshape(1, -1)
            
            with np.errstate(all='ignore'):
                features_scaled = scaler.transform(features_array)
                prediction = model.predict(features_scaled)
                probability = float(model.predict_proba(features_scaled)[0][1])
                
            # Second approval check
            if (prediction[0] == 1 and
                debt_to_income <= 40 and 
                income >= 20000 and 
                loan_amount <= income * 5):
                approved = True

        # Now 'approved' will be consistent for both storage and response
        loan_entry = Loan(
            user_id=current_user.id,
            income=float(income),
            loan_amount=float(loan_amount),
            loan_term=float(loan_term),
            employment_length=float(employment_length),
            decision='Approved' if approved else 'Denied',
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            email=current_user.email,
            phone=current_user.phone
        )
        
        db.session.add(loan_entry)
        db.session.commit()

        return jsonify({
            'approved': approved,
            'message': 'Loan approved!' if approved else 'Loan denied.',
            'metrics': {
                'debt_to_income': round(debt_to_income, 2),
                'loan_to_income': round(loan_to_income, 2),
                'employment_score': round(credit_history * 100, 2)
            }
        }), 200

    except Exception as e:
        logging.error(f"Error in predict route: {str(e)}")
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/api/loan-analytics', methods=['GET'])
@token_required
def get_loan_analytics(current_user):
    try:
        logging.info("Accessing loan analytics endpoint")
        
        if current_user.username != 'admin':
            logging.error("Non-admin user attempted to access analytics")
            return jsonify({'message': 'Admin access required'}), 403

        # Get analytics from the loan table directly
        total_applications = Loan.query.count()
        approved_count = Loan.query.filter_by(decision='Approved').count()
        denied_count = Loan.query.filter_by(decision='Denied').count()
        
        # Calculate approval rate
        approval_rate = (approved_count / total_applications * 100) if total_applications > 0 else 0
        
        # Calculate average loan amount
        avg_loan = db.session.query(
            func.avg(Loan.loan_amount)
        ).scalar() or 0

        result = {
            'total_applications': total_applications,
            'approved_count': approved_count,
            'denied_count': denied_count,
            'approval_rate': float(approval_rate),
            'avg_loan_amount': float(avg_loan),
            'last_updated': datetime.datetime.utcnow().isoformat()
        }

        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error in get_loan_analytics: {str(e)}")
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/api/test-freshdesk', methods=['GET'])
@token_required
def test_freshdesk(current_user):
    try:
        # Use the hardcoded credentials
        freshdesk_api_key = 'BKLJtkXkZ2dA8W4gaW'
        freshdesk_domain = 'stiegler.freshdesk.com'
        
        # Create base64 encoded auth string
        auth_str = base64.b64encode(f"{freshdesk_api_key}:X".encode()).decode()
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {auth_str}'
        }
        
        test_url = f'https://{freshdesk_domain}/api/v2/tickets'
        
        response = requests.get(test_url, headers=headers)
        
        logging.info(f"Freshdesk test response status: {response.status_code}")
        logging.info(f"Freshdesk test response: {response.text[:200]}")  # Log first 200 chars
        
        return jsonify({
            'status': 'success',
            'freshdesk_status': response.status_code,
            'container_status': {
                'db_connected': db.session.is_active,
                'freshdesk_connected': response.ok
            },
            'domain': freshdesk_domain
        }), 200
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Freshdesk connection error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'container_status': {
                'db_connected': db.session.is_active,
                'freshdesk_connected': False
            }
        }), 500

@app.route('/api/create-ticket', methods=['POST'])
@token_required
def create_ticket(current_user):
    try:
        data = request.get_json()
        freshdesk_api_key = 'BKLJtkXkZ2dA8W4gaW'
        freshdesk_domain = 'stiegler.freshdesk.com'
        
        auth_str = base64.b64encode(f"{freshdesk_api_key}:X".encode()).decode()
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {auth_str}'
        }
        
        ticket_data = {
            'subject': data.get('subject'),
            'description': data.get('description'),
            'email': current_user.email or data.get('email'),
            'priority': 1,
            'status': 2
        }
        
        response = requests.post(
            f'https://{freshdesk_domain}/api/v2/tickets',
            headers=headers,
            json=ticket_data
        )
        
        if response.status_code == 201:
            return jsonify({
                'status': 'success',
                'message': 'Ticket created successfully',
                'ticket': response.json()
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to create ticket: {response.text}'
            }), response.status_code
            
    except Exception as e:
        logging.error(f"Error creating ticket: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/loan-applications/list', methods=['GET'])
@token_required
def get_loan_applications_list(current_user):
    try:
        logging.info("Accessing loan applications list endpoint")
        
        # Check if user is admin
        if current_user.username != 'admin':
            logging.error("Non-admin user attempted to access loan applications list")
            return jsonify({'message': 'Admin access required'}), 403

        # Query the database for all loan applications
        applications = Loan.query.with_entities(
            Loan.id,
            Loan.first_name,
            Loan.last_name,
            Loan.email,
            Loan.phone,
            Loan.loan_amount,
            Loan.decision,
            Loan.timestamp
        ).order_by(Loan.timestamp.desc()).all()

        # Format the results
        results = [{
            'id': app.id,
            'firstName': app.first_name,
            'lastName': app.last_name,
            'email': app.email,
            'phone': app.phone,
            'loanAmount': float(app.loan_amount),
            'status': app.decision.lower(),
            'timestamp': app.timestamp.isoformat()
        } for app in applications]

        return jsonify(results), 200

    except Exception as e:
        logging.error(f"Error in get_loan_applications_list: {str(e)}")
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/api/user/loans', methods=['GET'])
@token_required
def get_user_loans(current_user):
    try:
        # Get user's most recent loan application
        recent_loan = Loan.query.filter_by(user_id=current_user.id)\
            .order_by(Loan.timestamp.desc())\
            .first()
        
        # Get user's loan statistics
        user_loans = Loan.query.filter_by(user_id=current_user.id).all()
        total_applications = len(user_loans)
        total_amount = sum(loan.loan_amount for loan in user_loans)
        
        return jsonify({
            'firstName': current_user.first_name,
            'recentLoan': {
                'loan_amount': float(recent_loan.loan_amount),
                'loan_term': recent_loan.loan_term,
                'decision': recent_loan.decision,
                'timestamp': recent_loan.timestamp.isoformat()
            } if recent_loan else None,
            'stats': {
                'totalApplications': total_applications,
                'totalAmount': float(total_amount)
            }
        }), 200

    except Exception as e:
        logging.error(f"Error in get_user_loans: {str(e)}")
        return jsonify({'message': f'Error: {str(e)}'}), 500