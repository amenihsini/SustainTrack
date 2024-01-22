# transaction_record.py
from imports import *

class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = {'extend_existing': True}

    transaction_id = Column(String(36), primary_key=True)
    product_id = Column(String(36), ForeignKey('product.product_id'), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="transactions")

