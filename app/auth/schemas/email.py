from pydantic import BaseModel, field_validator ,EmailStr
import re

class ResetPasswordRequestSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    def validate_password(cls, v):
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", v):
            raise ValueError(
                "Password must be at least 8 characters long, contain one uppercase, one lowercase, one digit, and one special character."
            )
        return v