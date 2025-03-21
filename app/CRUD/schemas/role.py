from pydantic import BaseModel
from app.core.enums import RoleEnum

class RoleSchema(BaseModel):
    id: int
    name: RoleEnum 