from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "resume_evaluator")

# Global client instance
_client: AsyncIOMotorClient = None
_sync_client: MongoClient = None

def get_database():
    """
    Get the MongoDB database instance for synchronous operations.
    Returns a pymongo database object.
    """
    global _sync_client
    if _sync_client is None:
        _sync_client = MongoClient(MONGODB_URL)
    return _sync_client[DATABASE_NAME]

async def get_async_database():
    """
    Get the MongoDB database instance for asynchronous operations.
    Returns a motor database object.
    """
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(MONGODB_URL)
    return _client[DATABASE_NAME]

async def close_database_connection():
    """
    Close the database connections.
    """
    global _client, _sync_client
    if _client:
        _client.close()
        _client = None
    if _sync_client:
        _sync_client.close()
        _sync_client = None 