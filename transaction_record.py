# transaction_record.py
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from models import Base, Product  # Import Product and Base

class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = {'extend_existing': True}

    transaction_id = Column(String(36), primary_key=True)
    product_id = Column(String(36), ForeignKey('product.product_id'), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="transactions")
