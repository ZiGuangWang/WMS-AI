from fastapi import APIRouter, Depends
from app.db.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(db: AsyncIOMotorDatabase = Depends(get_database)):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 今日入库单
    today_inbound = await db["inbound_orders"].count_documents({"created_at": {"$gte": today}})
    
    # 今日出库单
    today_outbound = await db["outbound_orders"].count_documents({"created_at": {"$gte": today}})
    
    # 库存总量
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$quantity"}}}]
    inventory_total_res = await db["inventory"].aggregate(pipeline).to_list(length=1)
    inventory_total = inventory_total_res[0]["total"] if inventory_total_res else 0
    
    # 预警数量
    # Simple warning logic for now
    pipeline_warning = [
        {"$group": {"_id": "$goods_id", "total": {"$sum": "$quantity"}}}
    ]
    inv_totals = await db["inventory"].aggregate(pipeline_warning).to_list(length=1000)
    warning_count = 0
    for item in inv_totals:
        goods = await db["goods"].find_one({"_id": ObjectId(item["_id"])})
        if goods and item["total"] < goods.get("min_stock", 0):
            warning_count += 1
            
    return {
        "today_inbound": today_inbound,
        "today_outbound": today_outbound,
        "inventory_total": inventory_total,
        "warning_count": warning_count
    }
