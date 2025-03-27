import os
from fastapi import UploadFile, HTTPException
from pathlib import Path
from typing import List

# Base directory for file uploads
BASE_DIR = Path("uploads")
BASE_DIR.mkdir(exist_ok=True)

# Function to create a folder if it doesn't exist
def create_folder(folder_name: str):
    folder_path = BASE_DIR / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path

# Function to upload a file to the specified folder
def save_file(folder_name: str, file: UploadFile):
    folder_path = create_folder(folder_name)
    file_path = folder_path / file.filename

    # Save the file
    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())
    
    return {"message": f"File '{file.filename}' uploaded successfully to '{folder_name}'"}

# Function to list files in a folder
def list_files(folder_name: str) -> List[str]:
    folder_path = BASE_DIR / folder_name

    if not folder_path.exists():
        raise HTTPException(status_code=404, detail="Folder not found")
    
    return [f.name for f in folder_path.iterdir() if f.is_file()]

# Function to download a file
def get_file(folder_name: str, filename: str):
    file_path = BASE_DIR / folder_name / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return file_path

# Function to delete a file
def delete_file(folder_name: str, filename: str):
    file_path = BASE_DIR / folder_name / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path.unlink()
    return {"message": f"File '{filename}' deleted successfully"}
