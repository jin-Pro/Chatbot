# from openai import OpenAI

# openai_client = OpenAI(api_key="your-openai-api-key")

# def get_embedding(text: str) -> list[float]:
#     response = openai_client.embeddings.create(
#         input=[text],  # 리스트 형태로 보내는 것이 권장
#         model="text-embedding-3-small"
#     )
#     return response.data[0].embedding


from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    return model.encode(text).tolist()
