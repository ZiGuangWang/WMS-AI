from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .base import MongoBaseModel

class InboundItem(BaseModel):
    goods_id: str
    goods_name: str
    sku: str
    planned_quantity: int
    received_quantity: int = 0
    location_id: Optional[str] = None
    price: float = 0.0
    batch_no: Optional[str] = None
    expiry_date: Optional[datetime] = None

class InboundOrder(MongoBaseModel):
    order_no: str = Field(unique=True)
    type: str  # 采购入库, 退货入库, 其他入库
    supplier_id: str
    supplier_name: str
    items: List[InboundItem]
    status: int = 1  # 1: 待审核, 2: 待验收, 3: 待上架, 4: 已完成, 0: 已取消
    remark: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class InboundOrderCreate(BaseModel):
    type: str
    supplier_id: str
    supplier_name: str
    items: List[InboundItem]
    remark: Optional[str] = None

class InboundOrderUpdate(BaseModel):
    type: Optional[str] = None
    supplier_id: Optional[str] = None
    supplier_name: Optional[str] = None
    items: Optional[List[InboundItem]] = None
    status: Optional[int] = None
    remark: Optional[str] = None
