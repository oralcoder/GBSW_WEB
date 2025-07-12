# 베이스 이미지 설정
FROM python:3.11

# 컨테이너 내부의 메인 디렉토리 설정
WORKDIR /app

# Python package 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# app 폴더(Host의 app 디렉토리를 컨테이너의 app 디렉토리로 복사) 
# COPY ./app /app

# 서버 실행 명령
CMD ["python",  "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]