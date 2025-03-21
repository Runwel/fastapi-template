from sqlalchemy.orm import Session
from app.CRUD.models.role import Role
from app.core.enums import RoleEnum

def get_role_by_name(db: Session, role_name: RoleEnum):
    return db.query(Role).filter(Role.name == role_name).first()

def create_role(db: Session, role_name: RoleEnum):
    new_role = Role(name=role_name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role
