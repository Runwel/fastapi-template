from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.receipt_scanner import model, schema
import pytesseract
from PIL import Image
import re, os
from uuid import uuid4
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

router = APIRouter()

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' 

load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_API_KEY"))

# Define regular expressions for receipt data extraction
amount_regex = r"\b(?:PHP|\u20b1)?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b"
date_regex = r"\b(?:\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})\b"
ref_regex = r"(?:Ref(?:erence)? No[:.]?\s*)([A-Za-z0-9-]+)"

@router.post("/upload", response_model=schema.TransactionOut)
async def upload_receipt(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save file temporarily
    contents = await file.read()
    temp_path = f"temp_{uuid4()}.png"
    with open(temp_path, "wb") as f:
        f.write(contents)

    # OCR to extract text from the image
    image = Image.open(temp_path)
    text = pytesseract.image_to_string(image)

    # Extract amount, date, and reference number using regular expressions
    amount_match = re.search(amount_regex, text)
    date_match = re.search(date_regex, text)
    ref_match = re.search(ref_regex, text, re.IGNORECASE)

    amount = amount_match.group().replace(",", "") if amount_match else ""
    date = date_match.group() if date_match else ""
    ref_no = ref_match.group(1) if ref_match else ""

    if not (amount and date and ref_no):
        raise HTTPException(status_code=400, detail="Unable to extract complete receipt information.")

    # Upload the receipt image to Supabase storage
    bucket_name = "receipts"
    unique_filename = f"{uuid4()}_{file.filename}"  # Ensure unique filename
    file_path = temp_path  # Path of the temp file
    supabase.storage.from_(bucket_name).upload(unique_filename, file_path)  # Correct usage of upload method

    # Get the public URL after uploading the file
    file_url_response = supabase.storage.from_(bucket_name).get_public_url(unique_filename)

    # Directly access the URL from the response
    public_url = file_url_response['publicURL'] if isinstance(file_url_response, dict) else file_url_response

    # Save transaction details to the database
    transaction = model.Receipts(
        amount=amount,
        date=date,
        ref_no=ref_no,
        image_url=public_url,
        uploaded_at=datetime.utcnow()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Clean up temporary file
    os.remove(temp_path)

    # Return the extracted information and transaction details
    return schema.TransactionOut(
        id=transaction.id,
        amount=transaction.amount,
        date=transaction.date,
        ref_no=transaction.ref_no,
        image_url=transaction.image_url,
        uploaded_at=transaction.uploaded_at
    )