# Python 3.9 기반 이미지 사용
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 요구 사항 파일 복사
COPY requirements.txt /app/

# 의존성 설치
RUN pip install -r requirements.txt

# 애플리케이션 코드 복사
COPY . /app/

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
