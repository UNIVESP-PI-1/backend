from enum import Enum as PyEnum
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timezone

db = create_engine('sqlite:///base.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    def __init__(self, name, email, password, active = True, admin = False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active 
        self.admin = admin

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True))

    def __init__(self, name, description):
        self.name = name
        self.created_at = datetime.now(timezone.utc)
        self.description = description

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    sku = Column(String(50), unique=True, nullable=False)
    barcode = Column(String(50), nullable=True)

    cost_price = Column(Integer, nullable=False)
    sale_price = Column(Integer, nullable=False)

    stock_quantity = Column(Integer, nullable=True, default=0)
    min_stock = Column(Integer, nullable=True, default=0)

    status = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ProductFlow(Base):
    __tablename__ = 'product_flow'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, product_id, user_id, quantity, type, reason=None):
        self.product_id = product_id
        self.user_id = user_id
        self.quantity = abs(int(quantity))
        self.type = type
