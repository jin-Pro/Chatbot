from openai import OpenAI
openai_client = OpenAI(api_key="your-openai-api-key")

def query_llm(prompt: str):
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content