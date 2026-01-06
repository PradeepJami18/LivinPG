from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from app.auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/qr")
async def upload_qr(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    file_location = f"static/qrcode.png"
    
    # Save file
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
        
    return {"message": "QR Code uploaded successfully", "url": "/static/qrcode.png"}
