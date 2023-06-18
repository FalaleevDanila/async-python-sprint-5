import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, ForeignKey
from sqlalchemy_utils import UUIDType

from src.db.db import Base


class File(Base):
    __tablename__ = 'file'
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid1)
    name = Column(String(50))
    created_ad = Column(DateTime(timezone=True), index=True, server_default=func.now())
    path = Column(String(100), unique=True, nullable=False)
    size = Column(Integer)
    is_downloadable = Column(Boolean, default=True)
    owner = Column(ForeignKey('user.id'), nullable=False)
