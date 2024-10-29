from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app import Loan, db  # Use your existing models
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set up database connection
DATABASE_URI = "postgresql://admin:admin@localhost:5432/admin"
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def extract_loan_data():
    loans = session.query(Loan).all()
    logging.info(f"Extracted {len(loans)} loan records.")
    return loans

def transform_loan_data(loans):
    total = len(loans)
    approved = sum(1 for loan in loans if loan.decision == 'Approved')
    denied = total - approved
    approval_rate = (approved / total) * 100 if total else 0
    avg_amount = sum(loan.loan_amount for loan in loans) / total if total else 0

    transformed_data = {
        'total_applications': total,
        'approved_count': approved,
        'denied_count': denied,
        'approval_rate': approval_rate,
        'avg_loan_amount': avg_amount,
        'last_updated': datetime.datetime.utcnow()
    }
    logging.info(f"Transformed data: {transformed_data}")
    return transformed_data

def load_analytics(data):
    with engine.connect() as connection:
        query = """
            INSERT INTO loan_analytics (total_applications, approved_count, denied_count, approval_rate, avg_loan_amount, last_updated)
            VALUES (%(total_applications)s, %(approved_count)s, %(denied_count)s, %(approval_rate)s, %(avg_loan_amount)s, %(last_updated)s)
        """
        connection.execute(query, data)
        logging.info("Data loaded into loan_analytics.")

def run_etl():
    loans = extract_loan_data()
    transformed_data = transform_loan_data(loans)
    load_analytics(transformed_data)

if __name__ == "__main__":
    run_etl()
