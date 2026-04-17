from pymongo import MongoClient
from app.core.config.settings import settings
from functools import lru_cache

class Database:
    client: MongoClient = None

db = Database()

def get_db_client():
    if db.client is None:
        db.client = MongoClient(settings.MONGODB_URL)
    return db.client

def get_database():
    client = get_db_client()
    return client[settings.DATABASE_NAME]
