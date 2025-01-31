# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, UserRole
import bcrypt

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

if __name__ == "__main__":
    init_db()
