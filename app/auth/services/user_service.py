from fastapi import HTTPException
from loguru import logger
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from app.auth.models.user import User
from app.auth.schemas.user import UserSchema
from app.auth.schemas.email import ResetPasswordSchema
from app.auth.services.role_service import get_role_by_name
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.email_service import send_email

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

def request_password_reset(db: Session, email: str):
    """Request password reset by sending email with reset link."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_token_data = {"sub": str(user.id)}  
    token = create_access_token(reset_token_data)  
    
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)
    db.commit()

    frontend_reset_link = f"sample.com/reset-password?token={token}"

    send_email(
        to=email,
        subject="Password Reset Request",
        body=f"Click the link below to reset your password:\n\n{frontend_reset_link}\n\nThis link will expire in 15 minutes."
    )

    return {"message": "Password reset link has been sent to your email."}

def reset_password_confirm(db: Session , token: str, reset_data: ResetPasswordSchema):
    user = db.query(User).filter(User.reset_token == token).first()

    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    reset_data = ResetPasswordSchema(
        new_password=reset_data.new_password,
        confirm_password=reset_data.confirm_password
    )

    user.password = hash_password(reset_data.new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()

    return {"message": "Password has been reset successfully"}

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
    user = db.query(User).filter(User.reset_token == token).first()

    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user.password = hash_password(reset_data.new_password)
    user.reset_token = None
    user.reset_token_expiry =  None
    db.commit()

    return {"messsage": "Password has been reset successfully"}