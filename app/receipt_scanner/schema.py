from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: str
    date: str
    ref_no: str
    image_url: str

class TransactionOut(TransactionCreate):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True