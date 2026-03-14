from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None
    perm_db = None

db = MongoDB()

async def connect_to_mongo():
    logging.info("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db.db = db.client[settings.DATABASE_NAME]
    # Connect to PermiHub-AI's database (default to 'permission_manager' from URI or explicitly)
    db.perm_db = db.client["permission_manager"]
    logging.info("Connected to MongoDB!")

async def close_mongo_connection():
    logging.info("Closing MongoDB connection...")
    db.client.close()
    logging.info("MongoDB connection closed!")

def get_database():
    if db.db is None:
        # Fallback for scripts or cases where lifespan didn't run
        client = AsyncIOMotorClient(settings.MONGODB_URI)
        db.db = client[settings.DATABASE_NAME]
    return db.db

def get_perm_database():
    if db.perm_db is None:
        # Fallback for PermiHub-AI database
        client = AsyncIOMotorClient(settings.MONGODB_URI)
        db.perm_db = client["permission_manager"]
    return db.perm_db
