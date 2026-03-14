from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .base import MongoBaseModel

class OutboundItem(BaseModel):
    goods_id: str
    goods_name: str
    sku: str
    planned_quantity: int
    picked_quantity: int = 0
    location_id: Optional[str] = None
    location_code: Optional[str] = None
    batch_no: Optional[str] = None

class OutboundOrder(MongoBaseModel):
    order_no: str = Field(unique=True)
    type: str  # 销售出库, 领用出库, 其他出库
    customer_name: str
    items: List[OutboundItem]
    status: int = 1  # 1: 待审核, 2: 待复核, 3: 待发货, 4: 已完成, 0: 已取消
    remark: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class OutboundOrderCreate(BaseModel):
    type: str
    customer_name: str
    items: List[OutboundItem]
    remark: Optional[str] = None

class OutboundOrderUpdate(BaseModel):
    type: Optional[str] = None
    customer_name: Optional[str] = None
    items: Optional[List[OutboundItem]] = None
    status: Optional[int] = None
    remark: Optional[str] = None
