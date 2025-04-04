from pydantic import BaseModel, Field
from typing import List, Literal

class RoleCreateSchema(BaseModel):
    name: str  
    permissions: List[Literal["CREATE", "READ", "UPDATE", "DELETE"]] = Field(
        example=["CREATE", "READ", "UPDATE", "DELETE"]  
    )

    class Config:
        orm_mode = True 
