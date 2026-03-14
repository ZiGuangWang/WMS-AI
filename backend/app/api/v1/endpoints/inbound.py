from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.db.mongodb import get_database
from app.models.inbound import InboundOrder, InboundOrderCreate, InboundOrderUpdate
from app.models.inventory import Inventory, InventoryLog
from .crud_helper import CRUD
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

router = APIRouter()

inbound_crud = CRUD("inbound_orders")

@router.get("/orders", response_model=List[InboundOrder])
async def list_orders(
    order_no: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    query = {}
    if order_no: query["order_no"] = {"$regex": order_no, "$options": "i"}
    if type: query["type"] = type
    if status is not None: query["status"] = status
    return await inbound_crud.get_all(db, query, skip, limit)

@router.post("/orders", response_model=InboundOrder, status_code=status.HTTP_201_CREATED)
async def create_order(data: InboundOrderCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Generate Order No: IN + timestamp
    order_no = f"IN{datetime.now().strftime('%Y%m%d%H%M%S')}"
    order_dict = data.model_dump()
    order_dict["order_no"] = order_no
    order_dict["status"] = 1  # 待审核
    return await inbound_crud.create(db, order_dict)

@router.get("/orders/{id}", response_model=InboundOrder)
async def get_order(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    order = await inbound_crud.get_one(db, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{id}", response_model=InboundOrder)
async def update_order(id: str, data: InboundOrderUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    updated = await inbound_crud.update(db, id, data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated

@router.post("/orders/{id}/audit")
async def audit_order(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    # 待审核 -> 待验收
    updated = await db["inbound_orders"].find_one_and_update(
        {"_id": ObjectId(id), "status": 1},
        {"$set": {"status": 2, "updated_at": datetime.now()}},
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=400, detail="Order not found or status invalid")
    return {"message": "Audit successful", "order": updated}

@router.post("/orders/{id}/receive")
async def receive_goods(id: str, items: List[dict], db: AsyncIOMotorDatabase = Depends(get_database)):
    # 待验收 -> 待上架
    # items list should contain updated received_quantity
    updated = await db["inbound_orders"].find_one_and_update(
        {"_id": ObjectId(id), "status": 2},
        {"$set": {"status": 3, "items": items, "updated_at": datetime.now()}},
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=400, detail="Order not found or status invalid")
    return {"message": "Receipt successful", "order": updated}

@router.post("/orders/{id}/shelve")
async def shelve_goods(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    # 待上架 -> 已完成
    order = await db["inbound_orders"].find_one({"_id": ObjectId(id), "status": 3})
    if not order:
        raise HTTPException(status_code=400, detail="Order not found or status invalid")
    
    # Update Stock
    for item in order["items"]:
        # Find inventory for this goods in this location
        # If no location assigned, we'll need a default one or error out.
        # Here we assume items have location_id and location_code
        if not item.get("location_id"):
            continue
            
        inv = await db["inventory"].find_one({
            "goods_id": item["goods_id"],
            "location_id": item["location_id"]
        })
        
        new_quantity = (inv["quantity"] if inv else 0) + item["received_quantity"]
        
        if inv:
            await db["inventory"].update_one(
                {"_id": inv["_id"]},
                {"$set": {"quantity": new_quantity, "updated_at": datetime.now()}}
            )
        else:
            # Get location code if not present
            loc = await db["locations"].find_one({"_id": ObjectId(item["location_id"])})
            new_inv = {
                "goods_id": item["goods_id"],
                "goods_name": item["goods_name"],
                "sku": item["sku"],
                "location_id": item["location_id"],
                "location_code": loc["code"] if loc else "Unknown",
                "quantity": item["received_quantity"],
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            await db["inventory"].insert_one(new_inv)
            
        # Log inventory change
        log = {
            "goods_id": item["goods_id"],
            "goods_name": item["goods_name"],
            "sku": item["sku"],
            "type": "入库",
            "order_no": order["order_no"],
            "location_id": item["location_id"],
            "location_code": item.get("location_code", "Unknown"),
            "change_quantity": item["received_quantity"],
            "after_quantity": new_quantity,
            "operator": "Admin",
            "created_at": datetime.now()
        }
        await db["inventory_logs"].insert_one(log)
        
        # Update location status to Partial or Full
        await db["locations"].update_one(
            {"_id": ObjectId(item["location_id"])},
            {"$set": {"status": 2}}  # 2: Partial
        )

    # Mark order as finished
    await db["inbound_orders"].update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": 4, "updated_at": datetime.now()}}
    )
    
    return {"message": "Shelving successful and stock updated"}
