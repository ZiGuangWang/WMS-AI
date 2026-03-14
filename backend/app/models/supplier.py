from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .base import MongoBaseModel

class Supplier(MongoBaseModel):
    name: str = Field(unique=True)
    contact_person: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    status: int = 1  # 1: Active, 0: Disabled
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class SupplierCreate(BaseModel):
    name: str
    contact_person: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: Optional[int] = None
