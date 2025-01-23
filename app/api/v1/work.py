from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session
from db.models import User, Work

router = APIRouter()

# # 엔드포인트: 특정 유저의 작품 조회
# @router.get("/work")
# def get_works(user_id: int, db: Session = Depends(get_db)):
#     # 유저 조회
#     user = db.query(User).filter(User.user_id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # 해당 유저의 작품들 조회
#     works = db.query(Work).filter(Work.user_id == user_id).all()
    
#     # 작품이 없다면, 빈 리스트 반환
#     if not works:
#         return {"message": "No works found for this user"}
    
#     # 작품 목록 반환
#     return {"user": user.username, "works": [work.title for work in works]}