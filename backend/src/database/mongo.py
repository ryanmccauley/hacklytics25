from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from settings import global_settings

client = AsyncIOMotorClient(global_settings.MONGO_CONNECTION_URI)
engine = AIOEngine(client, database="ctf")
