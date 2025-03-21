from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship
from app.core.db.session import Base
from app.core.enums import RoleEnum

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(RoleEnum), unique=True, index=True)
    users = relationship("User", back_populates="role")