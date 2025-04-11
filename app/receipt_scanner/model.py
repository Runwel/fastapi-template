from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.db.session import Base

class Receipts(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(String, nullable=False)
    date = Column(String, nullable=False)
    ref_no = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=func.now())