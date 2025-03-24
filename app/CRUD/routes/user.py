from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.CRUD.services.user_service import create_user, login_user
from app.core.db.session import get_db
from app.CRUD.schemas.user import UserCreateSchema, UserSchema, LoginRequestSchema
from app.core.security import admin_required

router = APIRouter()
# , dependencies=[Depends(admin_required)]
@router.post("/admin/users", response_model=UserSchema) 
def register_user_admin(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    return create_user(db, user_data)

@router.post("/auth/login")
def login_user_route(login_data: LoginRequestSchema, db: Session = Depends(get_db)):
    return login_user(db, login_data)