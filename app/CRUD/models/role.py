from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.orm import relationship
from app.core.db.session import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # ✅ Role name stored as a string
    permissions = Column(ARRAY(String), nullable=False, default=[])  # ✅ Stores permissions as an array of strings

    users = relationship("User", back_populates="role")  # ✅ Relationship with users
