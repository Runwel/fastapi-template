from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.services.admin_service import create_user_admin, approve_user, list_users
from app.core.db.session import get_db
from app.auth.dependencies import admin_or_dev_user
from app.auth.schemas.user import UserSchema
from app.auth.models.user import User

router = APIRouter()

@router.post("/users") 
def register_user_admin(user_data: UserSchema, db: Session = Depends(get_db), user: User = Depends(admin_or_dev_user)):
    return create_user_admin(db, user_data, user)

@router.put("/approve/{user_id}")
def approve_user_admin(user_id: int, status: str, db: Session = Depends(get_db), user: User = Depends(admin_or_dev_user)):
    return approve_user(db, user_id, status, user)

@router.get("/users")
def get_all_user(db: Session = Depends(get_db), user: User = Depends(admin_or_dev_user)):
    return list_users(db, user)