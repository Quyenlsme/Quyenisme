from langchain.tools.retriever import create_retriever_tool
from langchain_core.documents import Document
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import FAISS

def create_retriever(db) -> EnsembleRetriever:
    FAISS_retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10},
    )

    documents_content = [doc.page_content for doc in db.similarity_search("", k=50)]
    bm25_retriever = BM25Retriever.from_texts(documents_content)
    bm25_retriever.k = 10

    ensemble_retriever = EnsembleRetriever(
        retrievers=[FAISS_retriever, bm25_retriever],
        weights=[0.7, 0.3],
    )
    return ensemble_retriever
