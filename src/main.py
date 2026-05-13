from contextlib import asynccontextmanager
from fastapi import FastAPI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from pinecone import Pinecone, ServerlessSpec
from routes import process, data, delete, ask
from dotenv import load_dotenv
import os
load_dotenv()

index_name = "rag-app"
models = {}

def init_pinecone():
    print("Initializing Pinecone...")
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    existing_indexes = [i.name for i in pc.list_indexes()]
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=3072,             
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")

    return pc


def load_embedding_model():
    print("Loading Gemini embedding model...")
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
    print("Gemini embedding model ready.")
    return embedding


def load_reranker():
    print("Loading cross-encoder reranker...")
    cross_encoder = HuggingFaceCrossEncoder(
        model_name="./models/reranker" 
    )

    print("Reranker ready.")
    return cross_encoder

def load_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.environ["GOOGLE_API_KEY"],
        temperature=0.3,
        convert_system_message_to_human=True,
    )
    print("LLM ready.")
    return llm


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    models["index"] = init_pinecone()
    models["embedding"] = load_embedding_model()
    models["reranker"] = load_reranker()
    models["llm"] = load_llm()

    app.state.models = models
    print("App is ready.")
    yield

    # shutdown
    models.clear()
    print("App shutdown.")


app = FastAPI(lifespan=lifespan)

app.include_router(data.data_router)
app.include_router(process.process_router)
app.include_router(ask.ask_router)
app.include_router(delete.delete_router)

