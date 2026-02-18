import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
from config import REDIS_URL, MONGO_URI

redis_client = redis.from_url(REDIS_URL, decode_responses=True)
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["chatfight"]
