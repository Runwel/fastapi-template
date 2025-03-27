from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.services.role_service import (
    create_role, update_role_permissions, get_all_roles, delete_role
)
from app.core.db.session import get_db
from app.auth.schemas.role import RoleCreateSchema, RoleSchema
from typing import List

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RoleSchema)
def add_role(role_data: RoleCreateSchema, db: Session = Depends(get_db)):
    role = create_role(db, role_data.name, role_data.permissions)
    if not role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return role

@router.put("/{role_id}", response_model=RoleSchema)
def update_role(role_id: int, permissions: List[str], db: Session = Depends(get_db)):
    role = update_role_permissions(db, role_id, permissions)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/", response_model=List[RoleSchema])
def get_roles(db: Session = Depends(get_db)):
    return get_all_roles(db)

@router.delete("/{role_id}", response_model=RoleSchema)
def remove_role(role_id: int, db: Session = Depends(get_db)):
    role = delete_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
