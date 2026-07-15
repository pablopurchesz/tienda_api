from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)

    orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_email = Column(String(200), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(20), nullable=True, server_default="pending")
    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now())

    product = relationship("Product", back_populates="orders")
