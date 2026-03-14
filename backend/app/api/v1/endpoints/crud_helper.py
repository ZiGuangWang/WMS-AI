from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from app.db.mongodb import get_database
from bson import ObjectId
from datetime import datetime

class CRUD:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    async def get_all(self, db, query: dict = {}, skip: int = 0, limit: int = 100) -> List[dict]:
        cursor = db[self.collection_name].find(query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_by_id(self, db, id: str) -> Optional[dict]:
        if not ObjectId.is_valid(id):
            return None
        return await db[self.collection_name].find_one({"_id": ObjectId(id)})

    async def create(self, db, data: dict) -> dict:
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        result = await db[self.collection_name].insert_one(data)
        data["_id"] = result.inserted_id
        return data

    async def update(self, db, id: str, data: dict) -> Optional[dict]:
        if not ObjectId.is_valid(id):
            return None
        data["updated_at"] = datetime.now()
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": data},
            return_document=True
        )
        return result

    async def delete(self, db, id: str) -> bool:
        if not ObjectId.is_valid(id):
            return False
        result = await db[self.collection_name].delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    async def count(self, db, query: dict = {}) -> int:
        return await db[self.collection_name].count_documents(query)
