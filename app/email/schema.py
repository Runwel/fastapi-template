from typing import Optional
from pydantic import BaseModel
from pydantic import Field
from typing_extensions import Annotated
from datetime import datetime


class EmailSchema(BaseModel):
    recipient: str = Field(example="user@example.com")
    subject: str = Field(example="Welcome to our platform!")
    body: str = Field(example="Dear user,\n\nThank you for signing up...")
    sent_at: Optional[datetime] = Field(default=None, example="2025-03-20T19:00:00")
    is_sent: bool = Field(default=False, example=True)

    class Config:
        json_schema_extra = {
            "example": {
                "recipient": "test@example.org",
                "subject": "Important Announcement",
                "body": "This is the content of the important announcement.",
                "sent_at": "2025-03-21T10:30:00",
                "is_sent": False,
            }
        }


class EmailCreate(EmailSchema):
    # When creating, we might not have sent_at or is_sent yet
    sent_at: Optional[datetime] = None
    is_sent: bool = False


class EmailRead(EmailSchema):
    id: int = Field(example=1)
    sent_at: datetime  # Ensure sent_at is always present in the read model


class EmailUpdate(BaseModel):
    recipient: Optional[str] = Field(default=None, example="updated@example.com")
    subject: Optional[str] = Field(default=None, example="Updated Subject")
    body: Optional[str] = Field(default=None, example="Updated email content.")
    is_sent: Optional[bool] = Field(default=None, example=True)