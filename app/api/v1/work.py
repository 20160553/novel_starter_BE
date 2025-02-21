from typing import Optional

from fastapi import FastAPI, Header, Depends, HTTPException, Query, APIRouter
from service.service_helper import service_dict
from core.utils.jwt import verify_token
from schemas.models import WorkCreate

router = APIRouter()

#특정 유저의 작품 조회
@router.get("/{user_id}")
async def get_works_by_user_id(user_id: int):
    getUserTask = service_dict.get('User').get("get_user_by_id")
    user = getUserTask(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    getWorksTask = service_dict.get('Work').get("get_works_by_user_id")
    works = getWorksTask(user_id)
    return works

#특정 유저의 작품 추가
@router.post("/")
async def create_work(work: WorkCreate, authorization: Optional[str] = Header(None)):
    payload = verify_token(authorization.split(' ')[1])
    
    if (payload == None):
        raise HTTPException(status_code=401, detail="AccessToken is strange!")
    
    addWorkTask = service_dict.get('Work').get("add_work")
    
    newWork = WorkCreate(title=work.title, description=work.description, user_id=payload['id'])
    
    result = addWorkTask(work)
    
    return result