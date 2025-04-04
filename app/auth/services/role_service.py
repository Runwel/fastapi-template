from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.auth.models.role import Role
from app.auth.models.user import User
from app.auth.models.audit_logs import AuditLog
from typing import List
from app.auth.schemas.role import RoleCreateSchema

PROTECTED_ROLES = {"ADMIN", "DEVELOPER"}

def get_role_by_name(db: Session, role_name: str):
    return db.query(Role).filter(Role.name == role_name).first()

def create_role(db: Session, role_name: str, permissions: List[str], user: User):
    """Creates a new role with permissions."""
    
    if get_role_by_name(db, role_name):
        raise HTTPException(status_code=400, detail="Role already exists")

    valid_permissions = {"CREATE", "READ", "UPDATE", "DELETE"}
    if permissions is None or not permissions:
        permissions = ["READ"]

    if not all(p in valid_permissions for p in permissions):
        raise HTTPException(status_code=400, detail="Invalid permissions provided")

    new_role = Role(name=role_name, permissions=permissions)

    # Debugging Print Statements
    print(f"Creating Role: {role_name} with Permissions: {permissions}")
    print(f"User Performing Action: {user.username}")

    try:
        audit_log = AuditLog(
            action=f"Created role '{role_name}' with permissions {permissions}",
            performed_by=user.username
        )
        
        db.add(audit_log)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)

        return new_role
    
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to create role")

def update_role_data(db: Session, role_id: int, role_data: RoleCreateSchema, user: User):
    """Updates the name and permissions of an existing role."""

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role_data.name and role_data.name != role.name:
        existing_role = db.query(Role).filter(Role.name == role_data.name).first()
        if existing_role:
            raise HTTPException(status_code=400, detail="Role name already exists")

    if role_data.name:
        role.name = role_data.name
    if role_data.permissions is not None:
        valid_permissions = {"CREATE", "READ", "UPDATE", "DELETE"}
        if not all(p in valid_permissions for p in role_data.permissions):
            raise HTTPException(status_code=400, detail="Invalid permissions provided")
        role.permissions = role_data.permissions

    audit_log = AuditLog(
        action=f"Updated role '{role.name}' with permissions {role.permissions}",
        performed_by=user.username
    )
    db.add(audit_log)
    db.commit()
    db.refresh(role)

    return role

def delete_role(db: Session, role_id: int, user: User):
    """Delete a role unless it is in PROTECTED_ROLES and has no assigned users."""

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.name in PROTECTED_ROLES:
        raise HTTPException(status_code=403, detail=f"Cannot delete the '{role.name}' role")

    assigned_users = db.query(User).filter(User.role_id == role_id).count()
    if assigned_users > 0:
        raise HTTPException(status_code=400, detail=f"Cannot delete role '{role.name}' because {assigned_users} users are assigned to it.")

    db.delete(role)
    db.commit()

    audit_log = AuditLog(
        action=f"Deleted role '{role.name}'",
        performed_by=user.username,
    )
    db.add(audit_log)
    db.commit()

    return {
        "message": f"Role '{role.name}' deleted successfully",
        "deleted_role": {"id": role_id, "name": role.name},
        "deleted_by": user.username
    }

def get_all_roles(db: Session, user: User, limit: int = 10, offset: int = 0):
    """Retrieves all roles with pagination."""
    
    return db.query(Role).offset(offset).limit(limit).all()
