import os
import random
import time
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from assets.utils import set_vectorstore

index_name = "rag-app"





def chunk_folder(folder_path, chunk_size=500, chunk_overlap=50):

    all_documents = []

    # load all PDFs
    pdf_loader = DirectoryLoader(
        folder_path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
    )
    all_documents.extend(pdf_loader.load())

    # load all TXTs
    txt_loader = DirectoryLoader(
        folder_path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    all_documents.extend(txt_loader.load())

    loaded_files = list(set(
        os.path.basename(doc.metadata["source"])
        for doc in all_documents
        if "source" in doc.metadata
    ))

    print(f"Files loaded and chunked ({len(loaded_files)}):")
    for name in loaded_files:
        print(f"  - {name}")

    if not all_documents:
        raise ValueError(f"No PDF or TXT files found in: {folder_path}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    documents_texts = [rec.page_content for rec in all_documents]
    documents_metadata = [rec.metadata for rec in all_documents]

    chunks = text_splitter.create_documents(documents_texts, metadatas=documents_metadata)

    return chunks






## This function take a list of documents and upsert them to Pinecone in batches, with retry logic for rate limits.

def index_files(chunks, embeddings):
    BATCH_SIZE = 50
    WAIT_BETWEEN_BATCHES = 30

    local_vs = None

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        print(f"📤 Upserting batch {i//BATCH_SIZE + 1} / {-(-len(chunks)//BATCH_SIZE)} ({len(batch)} chunks)...")

        for attempt in range(5):
            try:
                if local_vs is None:
                    local_vs = PineconeVectorStore.from_documents(
                        documents=batch,
                        embedding=embeddings,
                        index_name=index_name,
                    )
                else:
                    local_vs.add_documents(batch)
                break

            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait = 60 * (attempt + 1) + random.randint(0, 10)
                    print(f"  ⚠️  Rate limited. Retrying in {wait}s (attempt {attempt+1}/5)...")
                    time.sleep(wait)
                else:
                    raise

        if i + BATCH_SIZE < len(chunks):
            print(f"  ⏳ Waiting {WAIT_BETWEEN_BATCHES}s before next batch...")
            time.sleep(WAIT_BETWEEN_BATCHES)

    set_vectorstore(local_vs)
    print("✅ All chunks upserted successfully")
    return local_vs