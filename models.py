# models.py

from datetime import datetime
from sqlalchemy import Column, String, Float, Date, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'

    product_id = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    expiration_date = Column(Date, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)
    quantity_sold = Column(Integer, default=0)
    quantity_purchased = Column(Integer, default=0)

    # Add this line to establish the relationship
    transactions = relationship("Transaction", back_populates="product")

    def is_approaching_expiration(self, days_threshold=7):
        today = datetime.utcnow().date()
        return (self.expiration_date - today).days <= days_threshold

class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(String(36), primary_key=True)
    product_id = Column(String(36), ForeignKey('product.product_id'), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="transactions")

