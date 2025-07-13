from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import os 
from service import pdf_parser, embedder, vector_store, prompt_builder, llm_client,text_splitter,fileController

router = APIRouter()


@router.get("/list-pdfs")
async def list_pdfs():
    directory = fileController.getDirPath()
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
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    path = fileController.save(file.filename,contents)
    
    # 1. 텍스트 추출 (PDF 내 텍스트)
    pdf_text = pdf_parser.extract_text_from_pdf(path)

    # 2. 이미지 OCR 텍스트 추출 (한글 설정)
    image_paths = pdf_parser.extract_images_from_pdf(path)
    ocr_text = pdf_parser.extract_text_from_images(image_paths, lang="kor")

    # 3. 전체 텍스트 병합
    full_text = pdf_text + "\n" + ocr_text

    # 4. 텍스트 분할 (정교하게)
    chunks = text_splitter.split_text(full_text)

    # 5. 임베딩 + 벡터 DB 저장
    embeddings = [embedder.get_embedding(chunk) for chunk in chunks]
    
    vector_store.save_to_vector_db(chunks, embeddings,file.filename)

    return 'success'


class DeleteRequest(BaseModel):
    filename: str

@router.delete("/delete-pdf/{filename}")
async def delete_pdf(filename:str):
    # 1. 파일 삭제
    dirPath = fileController.getDirPath()
    pdf_path = os.path.join(dirPath, filename)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF 파일이 존재하지 않습니다.")
    
    try:
        os.remove(pdf_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 삭제 실패: {str(e)}")

    # 2. 벡터 DB에서 관련 벡터 제거
    vector_store.delete(f"doc_{filename}_")

    return 'success'

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(payload: QuestionRequest):
    embedding = embedder.get_embedding(payload.question)
    context_chunks = vector_store.query_similar_chunks(embedding)
    prompt = prompt_builder.build_prompt(context_chunks, payload.question)
    answer = llm_client.query_llm(prompt)
    return {"answer": answer}