from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pickle
import numpy as np
import os

# Initialize Flask app and enable CORS for React frontend
app = Flask(__name__)
CORS(app)

# PostgreSQL configuration
POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'loan_db')

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database connection
db = SQLAlchemy(app)

# Loan Application model (for PostgreSQL)
class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_income = db.Column(db.Float, nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    credit_history = db.Column(db.Integer, nullable=False)
    prediction = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# Load the logistic regression model from the Pickle file
with open('loan_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Handle loan prediction requests."""
    data = request.json  # JSON data from React frontend
    features = np.array([[data['income'], data['loan_amount'], data['credit_history']]])

    # Make the prediction (0 = Denied, 1 = Approved)
    prediction = model.predict(features)
    result = 'Approved' if prediction[0] == 1 else 'Denied'

    # Store the result in the PostgreSQL database
    new_application = LoanApplication(
        applicant_income=data['income'],
        loan_amount=data['loan_amount'],
        credit_history=data['credit_history'],
        prediction=result
    )
    db.session.add(new_application)
    db.session.commit()

    # Return the result to the frontend
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
