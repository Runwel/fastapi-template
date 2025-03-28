from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.auth.models.user import User
from app.auth.schemas.user import UserSchema
from app.auth.services.role_service import get_role_by_name
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException
from loguru import logger

def create_user_admin(db: Session, user_data: UserSchema):
    
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
        birthdate=user_data.birthdate,
        status="approved",
        role=role 
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.success("Account created by Super Admin is created")
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Emailw or username already exists")

    return {
        "message": "Account creation successful",
        "user": {
            "username": new_user.username,
            "email": new_user.email,
            "rolename": role.name,
            "permission": role.permissions
        }
    }

def login_user(db: Session, login_data: UserSchema):

    user = db.query(User).filter(
        (User.email == login_data.email)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user.status != "approved":
        raise HTTPException(status_code=403, detail="Your account is not approved yet. Please wait for registrar approval.")

    role = user.role

    # Generate JWT token
    access_token = create_access_token(data={"sub": str(user.id), "role": role.name, "permissions": role.permissions})

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "username": user.username,
            "email": user.email,
            "status": user.status,
            "rolename": role.name,
            "permission": role.permissions
        }
    }
    
def register_user(db: Session, register_data: UserSchema):

    existing_user = db.query(User).filter(
        (User.username == register_data.username) | (User.email == register_data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already taken")
    
    role = get_role_by_name(db, register_data.role)

    hashed_password = hash_password(register_data.password)

    new_user = User(
        username=register_data.username,
        email=register_data.email,
        password=hashed_password,
        birthdate=register_data.birthdate,
        status="pending",
        role=role
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.success("User registered with pending status")
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or username already exists")

    return {
        "message": "Registration submitted. Awaiting approval.",
        "user": {
            "username": new_user.username,
            "email": new_user.email,
            "status": new_user.status
        }
    }

def approve_user(db: Session, user_id: int, status: str):
    if status not in ["approved", "pending"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.status == "approved":
        raise HTTPException(status_code=400, detail="User is already approved")

    user.status = status
    db.commit()

    return {
        "message": f" User status updated to {status}",
        "user": {
            "id": user.id,
            "username": user.username,
            "status": user.status
        }
    }

def list_users(db: Session, status: str = "all"):

    query = db.query(User)

    if status in ["pending", "approved"]:
        query = query.filter(User.status == status)

    users = query.all()

    return {
        "users": [{"id": u.id, "username": u.username, "status": u.status} for u in users]
    }

# def google_login(db: Session, google_token: str):
#     """Authenticate using Google OAuth2 token and return JWT."""

#     user_data = verify_google_oauth2_token(google_token)
#     if not user_data:
#         raise HTTPException(status_code=401, detail="Invalid Google authentication token")

#     email = user_data.get("email")
#     name = user_data.get("name")
#     google_id = user_data.get("sub")  # Unique Google user ID

#     # Check if user already exists
#     user = db.query(User).filter(User.email == email).first()

#     if not user:
#         # Auto-register Google users with default role
#         default_role = get_role_by_name(db, "GUEST")

#         user = User(
#             username=name,
#             email=email,
#             google_id=google_id,  # Store Google ID
#             status="approved",
#             role=default_role
#         )
#         db.add(user)
#         db.commit()
#         db.refresh(user)

#     # Generate JWT token
#     access_token = create_access_token(data={"sub": user.id, "role": user.role.name, "permissions": user.role.permissions})

#     return {
#         "message": "Google login successful",
#         "access_token": access_token,
#         "token_type": "bearer",
#         "user": {
#             "username": user.username,
#             "email": user.email,
#             "status": user.status,
#             "rolename": user.role.name,
#             "permission": user.role.permissions
#         }
#     }