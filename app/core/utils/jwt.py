import jwt
from datetime import datetime, timedelta
from pytz import timezone
from typing import Optional
from core.config import Config

ALGORITHM = "HS256"
SECRET_KEY = Config.JWT_SECRET_KEY # 비밀 키는 안전하게 관리해야 합니다.
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 토큰 만료 시간 (30분)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone('Asia/Seoul')) + expires_delta
    else:
        expire = datetime.now(timezone('Asia/Seoul')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
