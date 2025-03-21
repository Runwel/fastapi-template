from pydantic import BaseModel
from app.CRUD.schemas.role import RoleSchema

# ✅ Schema for creating a user (includes password)
class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str  # ✅ Include password
    role: RoleSchema

# ✅ Schema for returning user data (excludes password)
class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    role: RoleSchema

    class Config:
        orm_mode = True  # ✅ Allows SQLAlchemy to work with Pydantic
