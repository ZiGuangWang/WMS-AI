from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.db.mongodb import get_database
from app.models.outbound import OutboundOrder, OutboundOrderCreate, OutboundOrderUpdate
from app.models.inventory import Inventory, InventoryLog
from .crud_helper import CRUD
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

router = APIRouter()

outbound_crud = CRUD("outbound_orders")

@router.get("/orders", response_model=List[OutboundOrder])
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
    return await outbound_crud.get_all(db, query, skip, limit)

@router.post("/orders", response_model=OutboundOrder, status_code=status.HTTP_201_CREATED)
async def create_order(data: OutboundOrderCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Generate Order No: OUT + timestamp
    order_no = f"OUT{datetime.now().strftime('%Y%m%d%H%M%S')}"
    order_dict = data.model_dump()
    order_dict["order_no"] = order_no
    order_dict["status"] = 1  # 待审核
    return await outbound_crud.create(db, order_dict)

@router.put("/orders/{id}", response_model=OutboundOrder)
async def update_order(id: str, data: OutboundOrderUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    updated = await outbound_crud.update(db, id, data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated

@router.post("/orders/{id}/audit")
async def audit_order(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    # 待审核 -> 待复核
    updated = await db["outbound_orders"].find_one_and_update(
        {"_id": ObjectId(id), "status": 1},
        {"$set": {"status": 2, "updated_at": datetime.now()}},
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=400, detail="Order not found or status invalid")
    return {"message": "Audit successful", "order": updated}

@router.post("/orders/{id}/review")
async def review_goods(id: str, items: List[dict], db: AsyncIOMotorDatabase = Depends(get_database)):
    # 待复核 -> 待发货
    # items list should contain updated picked_quantity and location_id
    updated = await db["outbound_orders"].find_one_and_update(
        {"_id": ObjectId(id), "status": 2},
        {"$set": {"status": 3, "items": items, "updated_at": datetime.now()}},
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=400, detail="Order not found or status invalid")
    return {"message": "Review successful", "order": updated}

@router.post("/orders/{id}/ship")
async def ship_goods(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    # 待发货 -> 已完成
    order = await db["outbound_orders"].find_one({"_id": ObjectId(id), "status": 3})
    if not order:
        raise HTTPException(status_code=400, detail="Order not found or status invalid")
    
    # Update Stock
    for item in order["items"]:
        if not item.get("location_id"):
            continue
            
        inv = await db["inventory"].find_one({
            "goods_id": item["goods_id"],
            "location_id": item["location_id"]
        })
        
        if not inv or inv["quantity"] < item["picked_quantity"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient stock for {item['goods_name']} at {item.get('location_code', 'Unknown')}"
            )
            
        new_quantity = inv["quantity"] - item["picked_quantity"]
        
        await db["inventory"].update_one(
            {"_id": inv["_id"]},
            {"$set": {"quantity": new_quantity, "updated_at": datetime.now()}}
        )
            
        # Log inventory change
        log = {
            "goods_id": item["goods_id"],
            "goods_name": item["goods_name"],
            "sku": item["sku"],
            "type": "出库",
            "order_no": order["order_no"],
            "location_id": item["location_id"],
            "location_code": item.get("location_code", "Unknown"),
            "change_quantity": -item["picked_quantity"],
            "after_quantity": new_quantity,
            "operator": "Admin",
            "created_at": datetime.now()
        }
        await db["inventory_logs"].insert_one(log)
        
        # If quantity becomes 0, maybe update location status to Empty (1)
        if new_quantity == 0:
            # Check if other items exist in this location
            other_items = await db["inventory"].count_documents({
                "location_id": item["location_id"],
                "quantity": {"$gt": 0}
            })
            if other_items == 0:
                await db["locations"].update_one(
                    {"_id": ObjectId(item["location_id"])},
                    {"$set": {"status": 1}}  # 1: Empty
                )

    # Mark order as finished
    await db["outbound_orders"].update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": 4, "updated_at": datetime.now()}}
    )
    
    return {"message": "Shipping successful and stock deducted"}
