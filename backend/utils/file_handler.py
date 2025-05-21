## Saves Upload files
from fastapi import UploadFile
import os
import aiofiles

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_uploaded_files(file: UploadFile) -> str:
    save_path = os.path.join("uploads", file.filename)
    async with aiofiles.open(save_path, 'wb') as out_file:
        content = await file.read()  # async read file content
        await out_file.write(content)  # async write to disk
    return save_path