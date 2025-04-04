from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.services.user_service import login_user, register_user, request_password_reset, reset_password_confirm
from app.core.db.session import get_db
from app.auth.schemas.user import UserSchema, LoginSchema
from app.auth.schemas.email import ResetPasswordRequestSchema, ResetPasswordSchema

router = APIRouter()

@router.post("/login")
def login_user_route(login_data: LoginSchema, db: Session = Depends(get_db)):
    return login_user(db, login_data)

# @router.post("/google-login")
# def google_login_route(google_token: str, db: Session = Depends(get_db)):
#     return google_login(db, google_token)

@router.post("/register")
def register_user_route(register_data: UserSchema, db: Session = Depends(get_db)):
    return register_user(db, register_data)

@router.post("/reset-password")
def reset_password_request(reset_request: ResetPasswordRequestSchema, db: Session = Depends(get_db)):
    return request_password_reset(db, reset_request.email,)

@router.post("/reset-password/{token}")
def reset_password(token: str, reset_data: ResetPasswordSchema, db: Session = Depends(get_db)):
    return reset_password_confirm(db, token, reset_data)