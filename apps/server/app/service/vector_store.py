import chromadb
from chromadb.config import Settings

# persist_directory만 지정 (chroma_db_impl 옵션 제거)
settings = Settings(persist_directory="./vectorstore")

_client = chromadb.Client(settings=settings)
_collection = _client.get_or_create_collection(name="docs")



# from chromadb.config import Settings
# import chromadb

# settings = Settings(
#     persist_directory="./vectorstore"
# )

# client = chromadb.Client(settings=settings)

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