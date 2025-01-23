from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas.models import UserCreate, UserUpdate, UserResponse

from service.service_helper import service_dict

router = APIRouter()

# User 생성
@router.post("/users/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate):
    task = service_dict.get('User').get("add_user")
    result = task(user=user)
    return result

# @router.get("/", response_model=List[UserResponse])
# async def get_users(
#     user_id: Optional[list[int]] = Query(None),
#     name: Optional[list[str]] = Query(None),
#     email: Optional[list[str]] = Query(None),
#     is_active: Optional[bool] = Query(None),
# ):
#     task = service_dict.get('User').get("get_user_list")
#     result = task(
        
#     )
#     return result


@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(id: int):
    task = service_dict.get('User').get("get_user_by_id")
    result = task(id=id)
    return result


@router.put("/{id}", response_model=UserResponse)
async def update_user(id: int, user: UserUpdate):
    task = service_dict.get('User').get("update_user")
    result = task(id=id, update=user)
    return result


@router.delete("/{id}", response_model=None)
async def delete_user(id: int):
    task = service_dict.get('User').get("delete_user")
    result = task(id=id)
    return None