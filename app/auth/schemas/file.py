from pydantic import BaseModel, Field
from datetime import datetime


class FileSchema(BaseModel):
    folder_name: str = Field(..., min_length=1, max_length=255, example="documents")
    filename: str = Field(..., min_length=1, max_length=255, example="report.pdf")
    file_type: str = Field(..., max_length=100, example="application/pdf")
    file_size: int = Field(..., gt=0, example=1024)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
