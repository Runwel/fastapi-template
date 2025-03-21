from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.CRUD.services.role_service import create_role
from app.core.db.session import get_db
from app.CRUD.schemas.role import RoleSchema

router = APIRouter()

@router.post("/roles", response_model=RoleSchema)
def add_role(role_data: RoleSchema, db: Session = Depends(get_db)):
    return create_role(db, role_data.name)
