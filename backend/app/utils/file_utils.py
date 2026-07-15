"""File upload validation and safe storage to the uploads directory."""
import os
import uuid

from fastapi import UploadFile, HTTPException, status

from app.core.config import get_settings

settings = get_settings()

ALLOWED_EXTENSIONS = {"pdf", "docx"}


def validate_resume_file(file: UploadFile) -> str:
    """Validates extension; returns the lowercase extension (without dot)."""
    if not file.filename or "." not in file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File has no extension")

    extension = file.filename.rsplit(".", 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '.{extension}'. Only PDF and DOCX are allowed.",
        )
    return extension


def save_upload_file(file: UploadFile, extension: str) -> str:
    """
    Saves the uploaded file with a random filename (avoids collisions and
    path-traversal issues from user-supplied filenames) and enforces the
    max size limit while streaming to disk. Returns the saved file path.
    """
    os.makedirs(settings.upload_dir, exist_ok=True)

    unique_name = f"{uuid.uuid4().hex}.{extension}"
    dest_path = os.path.join(settings.upload_dir, unique_name)

    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    size = 0

    with open(dest_path, "wb") as out_file:
        while chunk := file.file.read(1024 * 1024):
            size += len(chunk)
            if size > max_bytes:
                out_file.close()
                os.remove(dest_path)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File exceeds max size of {settings.max_upload_size_mb}MB",
                )
            out_file.write(chunk)

    return dest_path
