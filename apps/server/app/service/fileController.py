import os

# 현재 파일 기준으로 프로젝트 루트 찾기 (예: main.py가 프로젝트 루트 하위에 있다고 가정)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def save(filename: str, contents: bytes):
    # 프로젝트 루트 아래 tmp 폴더에 저장
    save_dir = os.path.join(PROJECT_ROOT, "tmp")
    os.makedirs(save_dir, exist_ok=True)  # tmp 폴더가 없으면 생성

    path = os.path.join(save_dir, filename)
    with open(path, "wb") as f:
        f.write(contents)
    return path

def getDirPath():
    return os.path.join(PROJECT_ROOT, "tmp")