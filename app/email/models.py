from sqlalchemy import Column, Integer, DateTime, String, Boolean
from sqlalchemy.sql import func
from app.core.db.session import Base


class Email(Base):
    __tablename__ = "email"  # Fix: Use double underscores
    
    id = Column(Integer, primary_key=True)
    recipient = Column(String, index=True)
    subject = Column(String, index=True)
    body = Column(String)  # Assuming email body can be longer, not indexed
    sent_at = Column(DateTime, server_default=func.now())
    is_sent = Column(Boolean, default=False, index=True)

    class Config:
        orm_mode = True
