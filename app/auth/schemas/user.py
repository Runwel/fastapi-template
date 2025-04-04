from pydantic import BaseModel, field_validator, EmailStr, Field
from datetime import date, datetime
import re

class LoginSchema(BaseModel):
    email: EmailStr = Field(..., example="user123@example.com")
    password: str = Field(..., min_length=8, example="Secure@1234")

class UserSchema(BaseModel):
    username: str = Field(..., min_length=4, max_length=20, example="user123")
    email: EmailStr = Field(..., example="user123@example.com")
    password: str = Field(..., min_length=8, example="Secure@1234")
    birthdate: date = Field(..., example="2000-01-01")
    role: str = Field(..., example="STUDENT")

    # Alphanumeric only
    @field_validator("username")
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9 ]+$", v):
            raise ValueError("Username must be alphanumeric and may contain spaces, but no special characters")
        return v

    # Min 8 chars, upper, lower, digit, and special char
    @field_validator("password")
    def validate_password(cls, v):
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", v):
            raise ValueError(
                "Password must be at least 8 characters long, contain one uppercase, one lowercase, one digit, and one special character."
            )
        return v

    # User must be at least 18 years old
    @field_validator("birthdate")
    def validate_birthdate(cls, v):
        today = datetime.today().date()
        age = (today - v).days // 365
        if age < 18:
            raise ValueError("User must be at least 18 years old")
        return v

    class Config:
        orm_mode = True 
