from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.db.mongodb import get_database
from app.core.rbac import require_permissions
from app.models.inventory import Inventory, InventoryLog
from app.models.goods import Goods
from .crud_helper import CRUD
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime

router = APIRouter()

inventory_crud = CRUD("inventory")

@router.get("/query", response_model=List[Inventory])
async def query_inventory(
    goods_name: Optional[str] = None,
    sku: Optional[str] = None,
    location_code: Optional[str] = None,
    batch_no: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: AsyncIOMotorDatabase = Depends(get_database),
    _: None = Depends(require_permissions("wms:inventory:query:view")),
):
    query = {}
    if goods_name: query["goods_name"] = {"$regex": goods_name, "$options": "i"}
    if sku: query["sku"] = {"$regex": sku, "$options": "i"}
    if location_code: query["location_code"] = {"$regex": location_code, "$options": "i"}
    if batch_no: query["batch_no"] = {"$regex": batch_no, "$options": "i"}
    return await inventory_crud.get_all(db, query, skip, limit)

@router.get("/warning")
async def get_inventory_warning(
    db: AsyncIOMotorDatabase = Depends(get_database),
    _: None = Depends(require_permissions("wms:inventory:warning:view")),
):
    # Find goods where total inventory < min_stock
    # Aggregate inventory by goods_id
    pipeline = [
        {"$group": {"_id": "$goods_id", "total_quantity": {"$sum": "$quantity"}}}
    ]
    inventory_totals = await db["inventory"].aggregate(pipeline).to_list(length=1000)
    
    warnings = []
    for item in inventory_totals:
        goods = await db["goods"].find_one({"_id": ObjectId(item["_id"])})
        if goods and item["total_quantity"] < goods.get("min_stock", 0):
            warnings.append({
                "goods_id": str(goods["_id"]),
                "goods_name": goods["name"],
                "sku": goods["sku"],
                "current_stock": item["total_quantity"],
                "min_stock": goods["min_stock"],
                "status": "库存不足"
            })
    
    # Also find goods with 0 inventory that have min_stock > 0
    all_goods = await db["goods"].find({"min_stock": {"$gt": 0}}).to_list(length=1000)
    inventory_goods_ids = [item["_id"] for item in inventory_totals]
    for goods in all_goods:
        if str(goods["_id"]) not in [str(id) for id in inventory_goods_ids]:
            warnings.append({
                "goods_id": str(goods["_id"]),
                "goods_name": goods["name"],
                "sku": goods["sku"],
                "current_stock": 0,
                "min_stock": goods["min_stock"],
                "status": "无库存"
            })
            
    return warnings

@router.post("/adjust")
async def adjust_inventory(
    data: dict,
    db: AsyncIOMotorDatabase = Depends(get_database),
    _: None = Depends(require_permissions("wms:inventory:adjust:confirm")),
):
    goods_id = data.get("goods_id")
    location_id = data.get("location_id")
    adjust_quantity = data.get("adjust_quantity")
    remark = data.get("remark", "")
    
    if not all([goods_id, location_id, adjust_quantity is not None]):
        raise HTTPException(status_code=400, detail="Missing required fields")
        
    inv = await db["inventory"].find_one({
        "goods_id": goods_id,
        "location_id": location_id
    })
    
    if not inv:
        # Create new inventory record if adding
        if adjust_quantity <= 0:
            raise HTTPException(status_code=400, detail="Cannot subtract from non-existent inventory")
            
        goods = await db["goods"].find_one({"_id": ObjectId(goods_id)})
        loc = await db["locations"].find_one({"_id": ObjectId(location_id)})
        
        if not goods or not loc:
            raise HTTPException(status_code=404, detail="Goods or Location not found")
            
        new_inv = {
            "goods_id": goods_id,
            "goods_name": goods["name"],
            "sku": goods["sku"],
            "location_id": location_id,
            "location_code": loc["code"],
            "quantity": adjust_quantity,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        await db["inventory"].insert_one(new_inv)
        after_quantity = adjust_quantity
    else:
        after_quantity = inv["quantity"] + adjust_quantity
        if after_quantity < 0:
            raise HTTPException(status_code=400, detail="Resulting inventory cannot be negative")
            
        await db["inventory"].update_one(
            {"_id": inv["_id"]},
            {"$set": {"quantity": after_quantity, "updated_at": datetime.now()}}
        )
        goods_name = inv["goods_name"]
        sku = inv["sku"]
        location_code = inv["location_code"]

    # Log
    log = {
        "goods_id": goods_id,
        "goods_name": goods_name if inv else goods["name"],
        "sku": sku if inv else goods["sku"],
        "batch_no": inv.get("batch_no") if inv else None,
        "type": "调整",
        "order_no": f"ADJ{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "location_id": location_id,
        "location_code": location_code if inv else loc["code"],
        "change_quantity": adjust_quantity,
        "after_quantity": after_quantity,
        "operator": "Admin",
        "remark": remark,
        "created_at": datetime.now()
    }
    await db["inventory_logs"].insert_one(log)
    
    return {"message": "Inventory adjusted successfully", "after_quantity": after_quantity}

@router.get("/logs")
async def get_inventory_logs(
    goods_id: Optional[str] = None,
    type: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: AsyncIOMotorDatabase = Depends(get_database),
    _: None = Depends(require_permissions("wms:inventory:adjust:view")),
):
    query = {}
    if goods_id: query["goods_id"] = goods_id
    if type: query["type"] = type
    cursor = db["inventory_logs"].find(query).sort("created_at", -1).skip(skip).limit(limit)
    logs = await cursor.to_list(length=limit)
    # Convert ObjectId to string
    for log in logs:
        log["_id"] = str(log["_id"])
    return logs
