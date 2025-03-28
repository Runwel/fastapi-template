from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.services.user_service import create_user_admin, login_user, register_user, approve_user, list_users
from app.core.db.session import get_db
from app.auth.schemas.user import UserSchema, LoginSchema
from app.core.security import role_required
from app.auth.models.user import User

router = APIRouter()

# Admin protected routes
@router.post("/admin/users") 
def register_user_admin(user_data: UserSchema, db: Session = Depends(get_db), user: User = Depends(role_required(["ADMIN", "DEVELOPER"]))):
    return create_user_admin(db, user_data)

@router.put("/approve/{user_id}")
def approve_user_admin(user_id: int, status: str, db: Session = Depends(get_db), user: User = Depends(role_required(["ADMIN", "DEVELOPER"]))):
    return approve_user(db, user_id, status, user)

@router.get("/users")
def get_all_user(db: Session = Depends(get_db), user: User = Depends(role_required(["ADMIN", "DEVELOPER"]))):
    return list_users(db, user)

# Users routes
@router.post("/login")
def login_user_route(login_data: LoginSchema, db: Session = Depends(get_db)):
    return login_user(db, login_data)

# @router.post("/google-login")
# def google_login_route(google_token: str, db: Session = Depends(get_db)):
#     return google_login(db, google_token)

@router.post("/register")
def register_user_route(register_data: UserSchema, db: Session = Depends(get_db)):
    return register_user(db, register_data)