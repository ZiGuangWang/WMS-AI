from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .base import MongoBaseModel

class Inventory(MongoBaseModel):
    goods_id: str
    goods_name: str
    sku: str
    barcode: Optional[str] = None
    location_id: str
    location_code: str
    quantity: int = 0
    batch_no: Optional[str] = None
    expiry_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class InventoryLog(MongoBaseModel):
    goods_id: str
    goods_name: str
    sku: str
    batch_no: Optional[str] = None
    type: str  # 入库, 出库, 调整, 盘点
    order_no: Optional[str] = None
    location_id: str
    location_code: str
    change_quantity: int
    after_quantity: int
    operator: str = "Admin"
    created_at: datetime = Field(default_factory=datetime.now)
