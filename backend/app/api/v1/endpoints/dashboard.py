from fastapi import APIRouter, Depends
from app.db.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(db: AsyncIOMotorDatabase = Depends(get_database)):
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    
    # 辅助函数：计算趋势
    def calculate_trend(current, previous):
        if previous == 0:
            return 100 if current > 0 else 0
        return round((current - previous) / previous * 100, 1)

    # 1. 今日入库单
    today_inbound = await db["inbound_orders"].count_documents({"created_at": {"$gte": today_start}})
    yesterday_inbound = await db["inbound_orders"].count_documents({
        "created_at": {"$gte": yesterday_start, "$lt": today_start}
    })
    inbound_trend = calculate_trend(today_inbound, yesterday_inbound)
    
    # 2. 今日出库单
    today_outbound = await db["outbound_orders"].count_documents({"created_at": {"$gte": today_start}})
    yesterday_outbound = await db["outbound_orders"].count_documents({
        "created_at": {"$gte": yesterday_start, "$lt": today_start}
    })
    outbound_trend = calculate_trend(today_outbound, yesterday_outbound)
    
    # 3. 库存总量
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$quantity"}}}]
    inventory_total_res = await db["inventory"].aggregate(pipeline).to_list(length=1)
    inventory_total = inventory_total_res[0]["total"] if inventory_total_res else 0
    # 这里为了演示趋势，模拟一个对比值（实际可能需要每日库存快照表）
    inventory_trend = 0.5 # 模拟微增
    
    # 4. 预警数量
    pipeline_warning = [
        {"$group": {"_id": "$goods_id", "total": {"$sum": "$quantity"}}}
    ]
    inv_totals = await db["inventory"].aggregate(pipeline_warning).to_list(length=1000)
    warning_count = 0
    for item in inv_totals:
        goods = await db["goods"].find_one({"_id": ObjectId(item["_id"])})
        if goods and item["total"] < goods.get("min_stock", 0):
            warning_count += 1
    # 模拟预警趋势
    warning_trend = -2.0 # 模拟下降
            
    return {
        "today_inbound": {
            "value": today_inbound,
            "trend": inbound_trend,
            "status": "up" if inbound_trend > 0 else ("down" if inbound_trend < 0 else "neutral")
        },
        "today_outbound": {
            "value": today_outbound,
            "trend": outbound_trend,
            "status": "up" if outbound_trend > 0 else ("down" if outbound_trend < 0 else "neutral")
        },
        "inventory_total": {
            "value": inventory_total,
            "trend": inventory_trend,
            "status": "up" if inventory_trend > 0 else ("down" if inventory_trend < 0 else "neutral")
        },
        "warning_count": {
            "value": warning_count,
            "trend": warning_trend,
            "status": "up" if warning_trend > 0 else ("down" if warning_trend < 0 else "neutral")
        }
    }
