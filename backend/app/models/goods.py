from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .base import MongoBaseModel

class Goods(MongoBaseModel):
    name: str
    sku: str = Field(unique=True)
    barcode: Optional[str] = None
    category: Optional[str] = None
    unit: str
    spec: Optional[str] = None
    min_stock: int = 0
    supplier_id: Optional[str] = None
    price: float = 0.0
    status: int = 1  # 1: Active, 0: Disabled
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class GoodsCreate(BaseModel):
    name: str
    sku: str
    barcode: Optional[str] = None
    category: Optional[str] = None
    unit: str
    spec: Optional[str] = None
    min_stock: int = 0
    supplier_id: Optional[str] = None
    price: float = 0.0

class GoodsUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    spec: Optional[str] = None
    min_stock: Optional[int] = None
    supplier_id: Optional[str] = None
    price: Optional[float] = None
    status: Optional[int] = None
