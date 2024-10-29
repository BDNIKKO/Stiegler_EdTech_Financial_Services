from app import db, Loan, User
from datetime import datetime, timedelta

def create_test_data():
    try:
        # Create a test user if not exists
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            test_user = User(
                username='testuser',
                password='test123',
                first_name='Test',
                last_name='User',
                email='test@example.com',
                phone='123-456-7890'
            )
            db.session.add(test_user)
            db.session.commit()

        # Create some test loans with different decisions
        test_loans = [
            Loan(
                income=75000,
                loan_amount=250000,
                loan_term=30,
                employment_length=5,
                decision='Approved',
                timestamp=datetime.utcnow() - timedelta(days=1),
                user_id=test_user.id,
                first_name='Test',
                last_name='User',
                email='test@example.com',
                phone='123-456-7890'
            ),
            Loan(
                income=45000,
                loan_amount=300000,
                loan_term=15,
                employment_length=2,
                decision='Denied',
                timestamp=datetime.utcnow() - timedelta(hours=12),
                user_id=test_user.id,
                first_name='Test',
                last_name='User',
                email='test@example.com',
                phone='123-456-7890'
            ),
            Loan(
                income=120000,
                loan_amount=400000,
                loan_term=30,
                employment_length=10,
                decision='Approved',
                timestamp=datetime.utcnow(),
                user_id=test_user.id,
                first_name='Test',
                last_name='User',
                email='test@example.com',
                phone='123-456-7890'
            )
        ]

        for loan in test_loans:
            db.session.add(loan)
        
        db.session.commit()
        print("Test data created successfully!")
        
    except Exception as e:
        print(f"Error creating test data: {str(e)}")
        db.session.rollback()

if __name__ == "__main__":
    create_test_data() 