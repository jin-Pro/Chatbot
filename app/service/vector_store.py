import chromadb
from chromadb.config import Settings

_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./db"))
_collection = _client.get_or_create_collection(name="docs")

def get_vector_db():
    return _collection

def save_to_vector_db(chunks, embeddings, collection):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[f"doc_{i}"],
            embeddings=[embedding],
            documents=[chunk]
        )

def query_similar_chunks(query_embedding, collection, k: int = 5):
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results['documents'][0]