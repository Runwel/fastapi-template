from sqlalchemy import Column, Integer, Enum
from app.core.db.session import Base
from app.core.enums import PermissionEnum

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(PermissionEnum), unique=True, index=True)
