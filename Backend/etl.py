from app import db, Loan
import logging
from sqlalchemy import func
import datetime

def extract_loan_data():
    try:
        loans = Loan.query.all()
        logging.info(f"Extracted {len(loans)} loan records")
        return loans
    except Exception as e:
        logging.error(f"Error extracting loan data: {str(e)}")
        raise

def transform_loan_data(loans):
    if not loans:
        logging.info("No loan data available")
        return {
            'total_applications': 0,
            'approved_count': 0,
            'denied_count': 0,
            'approval_rate': 0,
            'avg_loan_amount': 0,
            'last_updated': datetime.datetime.utcnow()
        }

    total = len(loans)
    approved = sum(1 for loan in loans if loan.decision == 'Approved')
    denied = total - approved
    approval_rate = (approved / total) * 100 if total > 0 else 0
    avg_amount = sum(loan.loan_amount for loan in loans) / total if total > 0 else 0

    return {
        'total_applications': total,
        'approved_count': approved,
        'denied_count': denied,
        'approval_rate': approval_rate,
        'avg_loan_amount': avg_amount,
        'last_updated': datetime.datetime.utcnow()
    }

def load_analytics(data):
    try:
        sql = """
        INSERT INTO loan_analytics 
        (total_applications, approved_count, denied_count, approval_rate, avg_loan_amount, last_updated)
        VALUES (:total_applications, :approved_count, :denied_count, :approval_rate, :avg_loan_amount, :last_updated)
        """
        db.session.execute(sql, data)
        db.session.commit()
        logging.info("Analytics data loaded successfully")
    except Exception as e:
        logging.error(f"Error loading analytics data: {str(e)}")
        db.session.rollback()
        raise

def run_etl():
    try:
        logging.info("Starting ETL process...")
        loans = extract_loan_data()
        transformed_data = transform_loan_data(loans)
        load_analytics(transformed_data)
        logging.info("ETL process completed successfully")
    except Exception as e:
        logging.error(f"ETL process failed: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    run_etl()
