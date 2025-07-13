def build_prompt(context_chunks, question):
    context_block = "\n\n".join(context_chunks)
    prompt = f"""
[CONTEXT]
{context_block}

[QUESTION]
{question}

위 CONTEXT를 참고해서 QUESTION에 답변해주세요.
"""
    return prompt