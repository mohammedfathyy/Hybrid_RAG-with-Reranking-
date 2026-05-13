from langchain_pinecone import PineconeVectorStore

index_name = "rag-app"
_vectorstore = None

def get_vectorstore(pc, embeddings):
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = PineconeVectorStore(
            index=pc.Index(index_name),
            embedding=embeddings,
            text_key="text"
        )
    return _vectorstore

def set_vectorstore(vs):
    global _vectorstore
    _vectorstore = vs