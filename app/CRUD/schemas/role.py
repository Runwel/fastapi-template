from pydantic import BaseModel, Field
from typing import List, Literal

class RoleCreateSchema(BaseModel):
    name: str  
    permissions: List[Literal["CREATE", "READ", "UPDATE", "DELETE"]] = Field(
        example=["CREATE", "READ", "UPDATE", "DELETE"]  
    )

class RoleSchema(RoleCreateSchema):
    id: int 

    class Config:
        orm_mode = True  # ✅ Allows SQLAlchemy objects to be converted to Pydantic
