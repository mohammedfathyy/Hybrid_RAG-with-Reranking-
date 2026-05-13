from fastapi import FastAPI, UploadFile, APIRouter, HTTPException
from controller.DataController import validate_file
import os
import aiofiles


data_router = APIRouter()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@data_router.post("/upload")
async def upload_file(file: UploadFile):

    ##check file type and size
    is_valid, message = validate_file(file)

    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    
    ## save file to disk
    save_dir = os.path.join(BASE_DIR,"saved_data")
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, file.filename)
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(512000):  # Read in 500 KB chunks
                await f.write(chunk)
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    return {"message": message, "filename": file.filename}
    

    