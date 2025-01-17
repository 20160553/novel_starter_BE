from fastapi import FastAPI
import mysql.connector
import os
from dotenv import load_dotenv

# .env 파일을 로드
load_dotenv()

app = FastAPI()

# MySQL 연결 설정
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "rootpassword"),
        database=os.getenv("MYSQL_DB", "mydb")
    )
    return conn

# 기본 메시지 반환
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# 데이터베이스에서 데이터 조회
@app.get("/db")
async def read_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 'Hello, Docker!'")  # 실제 쿼리로 수정 가능
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"message": result[0]}
