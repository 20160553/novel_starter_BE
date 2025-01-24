from fastapi import APIRouter, Response, Depends, HTTPException
from schemas.models import UserCreate

from core.utils.jwt import create_access_token
from service.service_helper import service_dict

router = APIRouter()

@router.post("/login")
async def login(user: UserCreate, response: Response = Response()):
    task= service_dict.get('Login').get("login")
    result = task(user)
    
    if result==None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # JWT 토큰 생성
    access_token = create_access_token(data={
        "id": result.id,
        "username": result.username
        })
    
    # JWT 토큰을 Response Header에 넣어서 반환
    response.headers["Authorization"] = f"Bearer {access_token}"
    return {"message": "Login successful"}
