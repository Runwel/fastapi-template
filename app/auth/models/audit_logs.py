from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.db.session import Base

class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False )
    performed_by = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())