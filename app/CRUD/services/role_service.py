from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.CRUD.models.role import Role
from typing import List

PROTECTED_ROLES = {"ADMIN", "DEVELOPER"}

def get_role_by_name(db: Session, role_name: str):
    return db.query(Role).filter(Role.name == role_name).first()

def create_role(db: Session, role_name: str, permissions: List[str] = None):
    """Creates a new role with permissions."""
    
    if get_role_by_name(db, role_name):
        raise HTTPException(status_code=400, detail="Role already exists")

    valid_permissions = {"CREATE", "READ", "UPDATE", "DELETE"}
    if permissions is None or not permissions:
        permissions = ["READ"]

    if not all(p in valid_permissions for p in permissions):
        raise HTTPException(status_code=400, detail="Invalid permissions provided")

    new_role = Role(name=role_name, permissions=permissions)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def update_role_permissions(db: Session, role_id: int, permissions: List[str]):
    """Updates the permissions of an existing role."""
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    valid_permissions = {"CREATE", "READ", "UPDATE", "DELETE"}
    if not all(p in valid_permissions for p in permissions):
        raise HTTPException(status_code=400, detail="Invalid permissions provided")

    if not permissions:
        permissions = ["READ"] 

    role.permissions = permissions
    db.commit()
    return role

def delete_role(db: Session, role_id: int):
    """Delete a role unless it is in the PROTECTED_ROLES list."""
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.name in PROTECTED_ROLES:
        raise HTTPException(status_code=403, detail=f"Cannot delete the {role.name} role")

    db.delete(role)
    db.commit()
    return {"message": f"Role '{role.name}' deleted successfully"}

def get_all_roles(db: Session, limit: int = 10, offset: int = 0):
    """Retrieves all roles with pagination."""
    
    return db.query(Role).offset(offset).limit(limit).all()
