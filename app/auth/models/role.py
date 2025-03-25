from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.orm import relationship
from app.core.db.session import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  
    permissions = Column(ARRAY(String), nullable=False, default=[])  

    users = relationship("User", back_populates="role") 
