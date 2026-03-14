from fastapi import APIRouter
from app.api.v1.endpoints import basic_data

api_router = APIRouter()
api_router.include_router(basic_data.router, prefix="/basic", tags=["basic_data"])
