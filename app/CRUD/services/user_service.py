from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.CRUD.models.user import User
from app.CRUD.schemas.user import UserCreateSchema, UserSchema, LoginRequestSchema
from app.CRUD.services.role_service import get_role_by_name
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException

def create_user(db: Session, user_data: UserCreateSchema):
    
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")

    role = get_role_by_name(db, user_data.role)  # ✅ Now passing role as string
    
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        approved=True,
        role=role 
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or username already exists")

    return UserSchema(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        approved=new_user.approved,
        role=new_user.role.name 
    )

def login_user(db: Session, login_data: LoginRequestSchema):

    user = db.query(User).filter(
        (User.email == login_data.email)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
