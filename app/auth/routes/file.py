from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.auth.models.file import File as FileModel
from datetime import datetime
import os
from typing import List
from fastapi.responses import FileResponse

#Router and upload directory setup
router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#Utility functions for file management
def get_folder_path(folder_name: str) -> str:
    """Get or create folder path."""
    folder_path = os.path.join(UPLOAD_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_file_to_disk(folder_name: str, file: UploadFile) -> str:
    """Save the uploaded file to disk and return its path."""
    folder_path = get_folder_path(folder_name)
    file_location = os.path.join(folder_path, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return file_location

# Upload a file and save it in the database
@router.post("/upload")
async def upload_file(
    folder_name: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        file_location = save_file_to_disk(folder_name, file)

        # Save file metadata to the database
        db_file = FileModel(
            folder_name=folder_name,
            filename=file.filename,
            file_type=file.content_type,
            file_size=os.path.getsize(file_location),
            created_at=datetime.utcnow()
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return {
            "message": "File uploaded successfully",
            "file_id": db_file.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

# list all files in a folder (DB + Disk)
@router.get("/files/{folder_name}")
def list_folder_files(folder_name: str, db: Session = Depends(get_db)):
    try:
        # Fetch file metadata from DB
        db_files = db.query(FileModel).filter(FileModel.folder_name == folder_name).all()

        if not db_files:
            raise HTTPException(status_code=404, detail=f"No files found in folder '{folder_name}'")

        files = [
            {
                "id": file.id,
                "filename": file.filename,
                "file_type": file.file_type,
                "file_size": file.file_size,
                "created_at": file.created_at
            }
            for file in db_files
        ]

        return {
            "folder": folder_name,
            "files": files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

# Download a file by filename

@router.get("/download/{folder_name}/{filename}")
def download_file(folder_name: str, filename: str, db: Session = Depends(get_db)):
    try:
        # Verify the file exists in the DB
        db_file = db.query(FileModel).filter(
            FileModel.folder_name == folder_name,
            FileModel.filename == filename
        ).first()

        if not db_file:
            raise HTTPException(status_code=404, detail="File not found in database")

        # Verify the file exists on disk
        file_path = os.path.join(UPLOAD_DIR, folder_name, filename)

        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found on disk")

        # Set the original filename in the Content-Disposition header
        return FileResponse(
            file_path,
            headers={"Content-Disposition": f'attachment; filename="{db_file.filename}"'}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")

# Delete a file by filename (DB + Disk)
@router.delete("/delete/{folder_name}/{filename}")
def delete_file(folder_name: str, filename: str, db: Session = Depends(get_db)):
    try:
        # Delete from database
        db_file = db.query(FileModel).filter(
            FileModel.folder_name == folder_name,
            FileModel.filename == filename
        ).first()

        if not db_file:
            raise HTTPException(status_code=404, detail="File not found in database")

        db.delete(db_file)
        db.commit()

        # Delete from disk
        file_path = os.path.join(UPLOAD_DIR, folder_name, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

        return {"message": f"File '{filename}' deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")