from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.services.role_service import (
    create_role, update_role_permissions, get_all_roles, delete_role
)
from app.auth.models.user import User
from app.core.security import role_required
from app.core.db.session import get_db
from app.auth.schemas.role import RoleCreateSchema, RoleSchema
from typing import List

router = APIRouter()

@router.post("/", response_model=RoleSchema)
def add_role(role_data: RoleCreateSchema, db: Session = Depends(get_db), user: User = Depends(role_required(["ADMIN", "DEVELOPER"]))):
    role = create_role(db, role_data.name, role_data.permissions, user)
    if not role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return role

@router.put("/{role_id}", response_model=RoleSchema)
def update_role(role_id: int, permissions: List[str], db: Session = Depends(get_db), user: User = Depends(role_required(["ADMIN", "DEVELOPER"]))):
    role = update_role_permissions(db, role_id, permissions, user)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/", response_model=List[RoleSchema])
def get_roles(db: Session = Depends(get_db), user: User = Depends(role_required(["ADMIN", "DEVELOPER"]))):
    return get_all_roles(db, user)

@router.delete("/{role_id}", response_model=RoleSchema)
def remove_role(role_id: int, db: Session = Depends(get_db), user: User = Depends(role_required(["ADMIN", "DEVELOPER"]))):
    role = delete_role(db, role_id, user)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
