from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.email.models import Email
from app.email.schema import EmailCreate, EmailRead  # Assuming you'll create these schemas

router = APIRouter()

@router.post("/emails/", response_model=EmailRead, status_code=201)
def create_email(email_in: EmailCreate, db: Session = Depends(get_db)):
    """
    Creates a new email record.
    """
    db_email = Email(**email_in.model_dump())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email