from chromadb import PersistentClient  # 🔹 요거 필요
import uuid

_client = PersistentClient(path="/app/vectorstore")
_collection = _client.get_or_create_collection(name="docs")

def get_vector_db():
    return _collection

def save_to_vector_db(chunks, embeddings,filename):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        try:
            unique_id = str(uuid.uuid4())  # 항상 고유한 ID 생성
            _collection.add(
                ids=[f"doc_{filename}_{i}_{unique_id}"],
                embeddings=[embedding],
                documents=[chunk]
            )
            print(f"Added chunk {i}")
        except Exception as e:
            print(f"Error adding chunk {i}: {e}")

def query_similar_chunks(query_embedding, k: int = 5):
    results = _collection.query(query_embeddings=[query_embedding], n_results=k)
    return results['documents'][0]

def delete(target:str):
    results = _collection.get()

    # 관련 ID만 필터링
    related_ids = [doc_id for doc_id in results['ids'] if doc_id.startswith(target)]

    if related_ids:
        _collection.delete(ids=related_ids)
    
    return True
