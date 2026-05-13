import os
from fastapi import FastAPI, UploadFile, APIRouter, HTTPException, Request
from controller.ProcessController import chunk_folder, index_files

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

folder_path = os.path.join(BASE_DIR, "saved_data")

index_name = "RAG_APP"

process_router = APIRouter()
@process_router.get("/process")
async def process_files(request: Request):

    chunks = chunk_folder(folder_path=folder_path)
    vectorstore = index_files(chunks, embeddings=request.app.state.models["embedding"])

    request.app.state.chunks = chunks

    return {"message": "Files processed successfully", "chunks": len(chunks)}