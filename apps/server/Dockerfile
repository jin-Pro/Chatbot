FROM python:3.11
# FROM python:3.11-slim

WORKDIR /app

# requirements.txt 먼저 복사 → 캐시 활용
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# app 코드 복사
COPY ./app ./app
COPY ./vectorstore ./vectorstore

ENV PYTHONPATH=/app/app

# 실행 (command로 override 가능하므로 최소화)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
