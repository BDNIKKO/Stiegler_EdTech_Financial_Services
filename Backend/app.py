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

# Load the trained logistic regression model and scaler
model = pickle.load(open('models/logistic_model.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Extract the form data
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
    if employment_length > 5:
        credit_history = 1  # Good credit
    else:
        credit_history = 0  # Bad credit

    # Prepare the feature array for prediction
    input_features = np.array([[income, loan_amount, loan_term_months, employment_length, debt_to_income, loan_to_income, credit_history]])

    # Log input features for debugging
    print("Input features used for prediction:", input_features)

    # Scale the input
    scaled_input = scaler.transform(input_features)

    # Get the prediction from the model
    prediction = model.predict(scaled_input)[0]

    # Log the prediction result for debugging
    print("Prediction result:", prediction)

    # Return the prediction result as 'Approved' or 'Denied'
    result = 'Approved' if prediction == 1 else 'Denied'
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    with app.app_context():
        wait_for_db()  # Ensure database is ready before creating tables
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5000, debug=True)
