from fastapi import APIRouter, UploadFile, File,Form
from pydantic import BaseModel
from services import pdf_parser, embedder, vector_store, prompt_builder, llm_client



router = APIRouter()

class QuestionRequest(BaseModel):
    question: str


@router.get("/list-pdfs")
async def list_pdfs():
    directory = "/tmp"
    pdf_files = []

    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            size = os.path.getsize(file_path)  # 파일 크기 (바이트)
            pdf_files.append({
                "filename": filename,
                "size_bytes": size
            })

    return {"files": pdf_files}



@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    filename: str = Form(...)
):
    contents = await file.read()
    path = f"/tmp/{filename}"
    with open(path, "wb") as f:
        f.write(contents)

    # 1. 텍스트 추출 (PDF 내 텍스트)
    pdf_text = pdf_parser.extract_text_from_pdf("/tmp/uploaded.pdf")

    # 2. 이미지 OCR 텍스트 추출 (한글 설정)
    image_paths = pdf_parser.extract_images_from_pdf("/tmp/uploaded.pdf")
    ocr_text = pdf_parser.extract_text_from_images(image_paths, lang="kor")

    # 3. 전체 텍스트 병합
    full_text = pdf_text + "\n" + ocr_text

    # 4. 텍스트 분할 (정교하게)
    chunks = text_splitter.split_text(full_text)

    # 5. 임베딩 + 벡터 DB 저장
    embeddings = [embedder.get_embedding(chunk) for chunk in chunks]
    collection = vector_store.get_vector_db()
    vector_store.save_to_vector_db(chunks, embeddings, collection)

    return {"status": "uploaded"}

@router.post("/ask")
async def ask_question(payload: QuestionRequest):
    embedding = embedder.get_embedding(payload.question)
    collection = vector_store.get_vector_db()
    context_chunks = vector_store.query_similar_chunks(embedding, collection)
    prompt = prompt_builder.build_prompt(context_chunks, payload.question)
    answer = llm_client.query_llm(prompt)
    return {"answer": answer}