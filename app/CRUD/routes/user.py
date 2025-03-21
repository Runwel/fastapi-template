from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.CRUD.services.user_service import create_user
from app.core.db.session import get_db
from app.CRUD.schemas.user import UserCreateSchema, UserSchema

router = APIRouter()

@router.post("/users", response_model=UserSchema)  # ✅ Response should not include password
def register_user(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    return create_user(db, user_data)
