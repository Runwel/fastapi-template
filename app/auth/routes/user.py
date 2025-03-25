from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.services.user_service import create_user_admin, login_user, register_user, approve_user, list_users
from app.core.db.session import get_db
from app.auth.schemas.user import UserSchema
# from app.core.security import admin_requireds

router = APIRouter()
# Will be used in future functions for security purposes dependencies=[Depends(admin_required)]

@router.post("/admin/users", response_model=UserSchema) 
def register_user_admin(user_data: UserSchema, db: Session = Depends(get_db)):
    return create_user_admin(db, user_data)

@router.post("/auth/login")
def login_user_route(login_data: UserSchema, db: Session = Depends(get_db)):
    return login_user(db, login_data)
@router.post("/auth/register")
def register_user_route(register_data: UserSchema, db: Session = Depends(get_db)):
    return register_user(db, register_data)

@router.put("/approve/{user_id}", status_code=200)
def approve_user_admin(user_id: int, status: str, db: Session = Depends(get_db)):
    return approve_user(db, user_id, status)

@router.get("/users", status_code=200)
def get_all_user(user_id: int, status: str, db: Session = Depends(get_db)):
    return list_users(db, user_id, status)