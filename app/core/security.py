from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Security
from jose import jwt, JWTError
from app.core.config import settings
from sqlalchemy.orm import Session
from app.auth.models.user import User
from app.core.db.session import get_db
from datetime import datetime, timedelta, timezone
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="Authorization", auto_error=True)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(token: str = Security(api_key_header), db: Session = Depends(get_db)):
    """Get the current authenticated user from JWT token."""

    credentials_exception = HTTPException(status_code=401, detail="Invalid authentication credentials")

    try:
        parts = token.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise credentials_exception

        token_value = parts[1]

        payload = jwt.decode(token_value, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub") 
        role_name = payload.get("role")
        exp_timestamp = payload.get("exp")

        if user_id is None or role_name is None:
            raise credentials_exception
        
        try:
            user_id = int(user_id) 
        except ValueError:
            raise credentials_exception

        if exp_timestamp:
            now = datetime.now(timezone.utc).timestamp()
            if now > exp_timestamp:
                raise HTTPException(status_code=401, detail="Token has expired")

    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception

    user.role_name = role_name  
    return user

def role_required(allowed_roles: list[str]):
    """Dependency to check if user has the required role."""
    def _role_check(user: User = Depends(get_current_user)):
        if user.role_name not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access forbidden!")
        return user
    return _role_check

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
