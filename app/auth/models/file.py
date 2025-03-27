from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.db.session import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    folder_name = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(100))
    file_size = Column(Integer)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=func.now())
