from fastapi import HTTPException
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.auth.models.user import User
from app.auth.models.audit_logs import AuditLog
from app.auth.schemas.user import UserSchema
from app.auth.services.role_service import get_role_by_name
from app.core.security import hash_password

def create_user_admin(db: Session, user_data: UserSchema, created_by: User):
    
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")

    role = get_role_by_name(db, user_data.role)  
    
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

    audit_log = AuditLog(
        action=f"Created user {new_user.username}",
        performed_by=created_by.username
    )

    try:
        db.add(new_user)
        db.add(audit_log) 
        db.commit()
        db.refresh(new_user)

        logger.success(
            f"User {new_user.username} ({new_user.email}) created by {created_by.username} ({created_by.role.name})"
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email or username already exists")

    return {
        "message": "Account creation successful",
        "created_by": created_by.username,  # ✅ Returning who created the user
        "user": {
            "username": new_user.username,
            "email": new_user.email,
            "rolename": role.name,
            "permission": role.permissions
        }
    }

def approve_user(db: Session, user_id: int, status: str, user: User):
    if status not in ["approved", "pending"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if target_user.status == "approved":
        raise HTTPException(status_code=400, detail="User is already approved")

    target_user.status = status

    audit_log = AuditLog(
        action=f"Approved user {target_user.username} (ID: {target_user.id})",
        performed_by=user.username
    )

    try:
        db.add(audit_log)
        db.commit()
        db.refresh(target_user)

        logger.success(
            f"User {target_user.username} (ID: {target_user.id}) was approved by {user.username} ({user.role.name})"
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user status")

    return {
        "message": f"User status updated to {status}",
        "approved_by": user.username,
        "user": {
            "id": target_user.id,
            "username": target_user.username,
            "status": target_user.status
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
