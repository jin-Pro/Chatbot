FROM python:3.11-slim

WORKDIR /app

# 🧠 Tesseract OCR 설치 (언어팩 포함)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-kor \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# requirements 먼저 복사해서 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# PYTHONPATH 설정 (모듈 import를 위해)
ENV PYTHONPATH=/app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
