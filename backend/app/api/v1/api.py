from fastapi import APIRouter
from app.api.v1.endpoints import auth, basic_data, inbound, outbound, inventory, dashboard

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(basic_data.router, prefix="/basic", tags=["basic_data"])
api_router.include_router(inbound.router, prefix="/inbound", tags=["inbound"])
api_router.include_router(outbound.router, prefix="/outbound", tags=["outbound"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
