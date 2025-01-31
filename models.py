# models.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    DISTRIBUTOR = "distributor"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

class SalesRecord(Base):
    __tablename__ = 'sales_records'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    outlet_name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    owner_name = Column(String(100), nullable=False)
    contact_number = Column(String(15), nullable=False)
    gstin_un = Column(String(20), nullable=False)
    products_ordered = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_value = Column(Float, nullable=False)
    assigned_distributor_id = Column(Integer, ForeignKey('users.id'))
    payment_status = Column(String(20), default="pending")
    delivery_status = Column(String(20), default="pending")
    remarks = Column(String(200))

    assigned_distributor = relationship("User", foreign_keys=[assigned_distributor_id])
