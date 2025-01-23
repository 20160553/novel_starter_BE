import logging

from fastapi import FastAPI
from api.v1 import router as api_v1_router

logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(api_v1_router, prefix="/api/v1")