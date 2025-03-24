from pydantic import BaseModel

# ✅ Schema for creating a user (includes password)
class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str
    approved: bool
    role: str

# ✅ Schema for returning user data (excludes password)
class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    approved: bool
    role: str


class LoginRequestSchema(BaseModel):
    email: str 
    password: str  

    class Config:
        orm_mode = True 
