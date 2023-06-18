import uuid

from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType

from src.db.db import Base


class User(Base):
    __tablename__ = 'User'
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid1)
    name = Column(String(100), unique=True)
    password = Column(String(100), nullable=False)
    token = Column(String(100), unique=True)
