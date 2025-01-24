from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas.models import UserCreate, UserUpdate, UserResponse

from service.service_helper import service_dict

router = APIRouter()

# User 생성
@router.post("/users", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate):
    task = service_dict.get('User').get("add_user")
    result = task(user=user)
    return result

@router.get("/", response_model=List[UserResponse])
async def get_users(
    id: Optional[list[int]] = Query(None),
    username: Optional[list[str]] = Query(None),
):
    task = service_dict.get('User').get("get_user_list")
    result = task(
        id=id,
        username=username
    )
    return result


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

@router.get("/username_duplicated_check/{username}", response_model=bool)
async def username_duplicated_check(username: str):
    task= service_dict.get('User').get("get_user_by_username")
    result = task(username=username)
    if len(result) > 0:
        return True
    else :
        return False