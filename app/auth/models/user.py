from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from app.core.db.session import Base
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    birthdate = Column(DateTime, nullable=False)
    status = Column(Enum("pending", "approved", name="user_status"), default="pending")
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Reset Token for Password Reset 
    reset_token = Column(String, nullable=True, unique=True)
    reset_token_expiry = Column(DateTime, nullable=True)  # Expiration time for token

    def set_reset_token(self, token: str):
        """Stores the reset token and its expiry (1 hour validity)."""
        self.reset_token = token
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)

    role = relationship("Role", back_populates="users")
