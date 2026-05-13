##Sparse encoder & mix dense with sparse
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers.ensemble import EnsembleRetriever


##Reranking
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors.cross_encoder_rerank import CrossEncoderReranker


from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

def create_hybrid_Rank_retriever(vectorstore, cross_encoder, chunks):
    dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    keyword_retriever = BM25Retriever.from_documents(chunks)
    keyword_retriever.k = 5

    hybrid_retriever = EnsembleRetriever(retrievers=[dense_retriever, keyword_retriever], weights=[0.7,0.3])

    compressor = CrossEncoderReranker(model=cross_encoder, top_n=3)


    compression_retriever = ContextualCompressionRetriever(
        base_retriever=hybrid_retriever,
        base_compressor=compressor
    )

    print("Hybrid Rank Retriever created.")

    return compression_retriever


def Ask_Question(question, retriever, llm):

    prompt = ChatPromptTemplate.from_template("""
    You are an assistant. Answer the question using ONLY the context.
    If the answer is not in the context, say I don't know.

    Context:
    {context}

    Question:
    {input}

    Answer:
    """)

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)

    qa_chain = create_retrieval_chain(retriever, combine_docs_chain)

    response = qa_chain.invoke({"input": question})

    return response["answer"]