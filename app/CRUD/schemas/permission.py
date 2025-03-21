from pydantic import BaseModel
from app.core.enums import PermissionEnum

class PermissionSchema(BaseModel):
    id: int
    name: PermissionEnum