from fastapi import APIRouter

from .user import router as user_router
from .work import router as work_router

router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["User"])
router.include_router(work_router, prefix="/works", tags=["Work"])