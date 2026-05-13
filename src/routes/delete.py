from fastapi import APIRouter, Request
from controller.DeleteController import delete_files_in_folder
import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVED_DATA_DIR = os.path.join(BASEDIR, "saved_data")


delete_router = APIRouter()

@delete_router.delete("/delete")
async def delete_files(request: Request):
    result = delete_files_in_folder(folder_path=SAVED_DATA_DIR, pc=request.app.state.models["index"])
    return result