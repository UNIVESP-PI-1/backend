from enum import Enum as PyEnum
from sqlalchemy import create_engine, Enum,Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
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
    created_at = Column(DateTime(timezone=True))

    def __init__(self, name):
        self.name = name
        self.created_at = datetime.now(timezone.utc)

