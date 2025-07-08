from openai import OpenAI
openai_client = OpenAI(api_key="your-openai-api-key")

def get_embedding(text: str):
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding