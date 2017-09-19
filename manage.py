from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from models import get_uniq_name
from datetime import datetime


MONGO_IP = 'localhost'
MONGO_PORT = 27017

client = AsyncIOMotorClient(MONGO_IP, MONGO_PORT)

db = client.test_chat
collection = db.test_users


async def create_users():
	await collection.drop()
	for i in range(20):
		collection.insert({
			"_id": get_uniq_name(),
			"date": datetime.utcnow()
		})
	print(await collection.count())



loop = asyncio.get_event_loop()
loop.run_until_complete(create_users())
