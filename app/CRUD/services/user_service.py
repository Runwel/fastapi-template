from sqlalchemy.orm import Session
from app.CRUD.models.user import User
from app.CRUD.schemas.user import UserCreateSchema, UserSchema
from app.core.enums import RoleEnum
from app.CRUD.services.role_service import get_role_by_name
from app.core.security import hash_password  # ✅ Import password hashing function

def create_user(db: Session, user_data: UserCreateSchema):
    role = get_role_by_name(db, user_data.role.name)
    
    # ✅ Hash the password before storing
    hashed_password = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,  # ✅ Save hashed password
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user  # ✅ Return SQLAlchemy object, response_model handles schema conversion
