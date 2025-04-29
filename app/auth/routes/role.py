from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.services.role_service import (
    create_role, update_role_data, get_all_roles, delete_role
)
from app.auth.models.user import User
from app.core.db.session import get_db
# from app.auth.dependencies import admin_or_dev_user
from app.auth.schemas.role import RoleCreateSchema

router = APIRouter()

@router.post("/")
def add_role(role_data: RoleCreateSchema, db: Session = Depends(get_db)):
    role = create_role(db, role_data.name, role_data.permissions)
    if not role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return role

@router.put("/{role_id}")
def update_role(role_id: int, role_data: RoleCreateSchema, db: Session = Depends(get_db)):
    role = update_role_data(db, role_id, role_data)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.get("/")
def get_roles(db: Session = Depends(get_db)):
    return get_all_roles(db)

@router.delete("/{role_id}")
def remove_role(role_id: int, db: Session = Depends(get_db)):
    role = delete_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
