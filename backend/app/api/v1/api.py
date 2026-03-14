from fastapi import APIRouter
from app.api.v1.endpoints import basic_data, inbound

api_router = APIRouter()
api_router.include_router(basic_data.router, prefix="/basic", tags=["basic_data"])
api_router.include_router(inbound.router, prefix="/inbound", tags=["inbound"])
