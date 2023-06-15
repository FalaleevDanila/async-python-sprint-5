import uuid

from sqlalchemy import Column, String, UUID

from src.db.db import Base


class User(Base):
    __tablename__ = 'User'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True)
    password = Column(String(100), nullable=False)
    token = Column(String(100), unique=True)
