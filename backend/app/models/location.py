from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .base import MongoBaseModel

class Location(MongoBaseModel):
    code: str = Field(unique=True)  # e.g., A-01-01
    area: str  # e.g., Area A
    shelf: str  # e.g., Shelf 01
    bin: str  # e.g., Bin 01
    status: int = 1  # 1: Empty, 2: Partial, 3: Full, 0: Disabled
    remark: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class LocationCreate(BaseModel):
    code: str
    area: str
    shelf: str
    bin: str
    remark: Optional[str] = None

class LocationUpdate(BaseModel):
    code: Optional[str] = None
    area: Optional[str] = None
    shelf: Optional[str] = None
    bin: Optional[str] = None
    status: Optional[int] = None
    remark: Optional[str] = None
