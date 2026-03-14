from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.db.mongodb import get_database
from app.models.goods import Goods, GoodsCreate, GoodsUpdate
from app.models.location import Location, LocationCreate, LocationUpdate
from app.models.supplier import Supplier, SupplierCreate, SupplierUpdate
from .crud_helper import CRUD
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

router = APIRouter()

goods_crud = CRUD("goods")
location_crud = CRUD("locations")
supplier_crud = CRUD("suppliers")

# --- Goods Endpoints ---
@router.get("/goods", response_model=List[Goods])
async def list_goods(
    name: Optional[str] = None,
    sku: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    query = {}
    if name: query["name"] = {"$regex": name, "$options": "i"}
    if sku: query["sku"] = {"$regex": sku, "$options": "i"}
    return await goods_crud.get_all(db, query, skip, limit)

@router.post("/goods", response_model=Goods, status_code=status.HTTP_201_CREATED)
async def create_goods(data: GoodsCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Check for existing SKU
    existing = await db["goods"].find_one({"sku": data.sku})
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    return await goods_crud.create(db, data.dict())

@router.put("/goods/{id}", response_model=Goods)
async def update_goods(id: str, data: GoodsUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    updated = await goods_crud.update(db, id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Goods not found")
    return updated

@router.delete("/goods/{id}")
async def delete_goods(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not await goods_crud.delete(db, id):
        raise HTTPException(status_code=404, detail="Goods not found")
    return {"message": "Goods deleted successfully"}

# --- Location Endpoints ---
@router.get("/locations", response_model=List[Location])
async def list_locations(
    code: Optional[str] = None,
    area: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    query = {}
    if code: query["code"] = {"$regex": code, "$options": "i"}
    if area: query["area"] = area
    return await location_crud.get_all(db, query, skip, limit)

@router.post("/locations", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(data: LocationCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    existing = await db["locations"].find_one({"code": data.code})
    if existing:
        raise HTTPException(status_code=400, detail="Location code already exists")
    return await location_crud.create(db, data.dict())

@router.put("/locations/{id}", response_model=Location)
async def update_location(id: str, data: LocationUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    updated = await location_crud.update(db, id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Location not found")
    return updated

@router.delete("/locations/{id}")
async def delete_location(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not await location_crud.delete(db, id):
        raise HTTPException(status_code=404, detail="Location not found")
    return {"message": "Location deleted successfully"}

# --- Supplier Endpoints ---
@router.get("/suppliers", response_model=List[Supplier])
async def list_suppliers(
    name: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    query = {}
    if name: query["name"] = {"$regex": name, "$options": "i"}
    return await supplier_crud.get_all(db, query, skip, limit)

@router.post("/suppliers", response_model=Supplier, status_code=status.HTTP_201_CREATED)
async def create_supplier(data: SupplierCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    existing = await db["suppliers"].find_one({"name": data.name})
    if existing:
        raise HTTPException(status_code=400, detail="Supplier name already exists")
    return await supplier_crud.create(db, data.dict())

@router.put("/suppliers/{id}", response_model=Supplier)
async def update_supplier(id: str, data: SupplierUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    updated = await supplier_crud.update(db, id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return updated

@router.delete("/suppliers/{id}")
async def delete_supplier(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    if not await supplier_crud.delete(db, id):
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"message": "Supplier deleted successfully"}
