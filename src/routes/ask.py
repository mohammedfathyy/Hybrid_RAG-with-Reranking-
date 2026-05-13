import os
from urllib import request
from fastapi import FastAPI, UploadFile, APIRouter, HTTPException, Request
from controller.Retrieve_AskController import create_hybrid_Rank_retriever, Ask_Question
from assets.utils import get_vectorstore







ask_router = APIRouter()
@ask_router.get("/ask")
async def process_files(request: Request, question: str):

    cross_encoder = request.app.state.models["reranker"]
    pc = request.app.state.models["index"]
    llm = request.app.state.models["llm"]
    embedding = request.app.state.models["embedding"]

    chunks = request.app.state.chunks

    vectorstore = get_vectorstore(pc, embedding)
    retriever = create_hybrid_Rank_retriever(vectorstore, cross_encoder, chunks)  # Accessing the chunks directly from the ProcessController's index
    answer = Ask_Question(question, retriever, llm)
    return answer
