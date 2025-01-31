# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, SalesRecord, UserRole
import bcrypt
from datetime import date, timedelta
import random

# Database connection
DATABASE_URL = "postgresql://username:password@localhost/sales_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize database
def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Create pre-built users
    users = [
        {"username": "admin", "password": "12345", "role": UserRole.ADMIN},
        {"username": "distributor1", "password": "12345", "role": UserRole.DISTRIBUTOR},
        {"username": "distributor2", "password": "12345", "role": UserRole.DISTRIBUTOR},
    ]

    for user_data in users:
        hashed_password = bcrypt.hashpw(user_data["password"].encode("utf-8"), bcrypt.gensalt())
        user = User(username=user_data["username"], password=hashed_password.decode("utf-8"), role=user_data["role"])
        db.add(user)

    db.commit()
    db.close()

# Populate database with mock sales records
def populate_mock_data():
    db = SessionLocal()

    # Get distributor users
    distributors = db.query(User).filter(User.role == UserRole.DISTRIBUTOR).all()

    # Mock data for sales records
    outlets = ["Outlet A", "Outlet B", "Outlet C", "Outlet D", "Outlet E"]
    addresses = ["123 Main St", "456 Elm St", "789 Oak St", "101 Pine St", "202 Maple St"]
    owners = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Davis"]
    products = ["Product X", "Product Y", "Product Z"]
    statuses = ["pending", "done"]

    for i in range(20):  # Create 20 mock sales records
        record = SalesRecord(
            date=date.today() - timedelta(days=random.randint(0, 30)),  # Random date within the last 30 days
            outlet_name=random.choice(outlets),
            address=random.choice(addresses),
            owner_name=random.choice(owners),
            contact_number=f"123-456-789{i}",  # Unique contact number
            gstin_un=f"GSTIN{i:05d}",  # Unique GSTIN/UN
            products_ordered=random.choice(products),
            quantity=random.randint(1, 10),
            order_value=random.uniform(100.0, 1000.0),
            assigned_distributor_id=random.choice(distributors).id,
            payment_status=random.choice(statuses),
            delivery_status=random.choice(statuses),
            remarks=f"Mock record {i+1}"
        )
        db.add(record)

    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    populate_mock_data()
