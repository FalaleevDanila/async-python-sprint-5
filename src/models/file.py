import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UUID, func

from src.db.db import Base


class File(Base):
    __tablename__ = 'file'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50))
    created_ad = Column(DateTime(timezone=True), index=True, server_default=func.now())
    path = Column(String(100))
    size = Column(Integer)
    is_downloadable = Column(Boolean, default=True)
    owner = Column(ForeignKey('user.id', ondelete='SET NULL'))
