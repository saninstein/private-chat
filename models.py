from utils import get_uniq_name
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import datetime


class ModelException(Exception):
	pass


class NotFoundItem(ModelException):
	def __init__(self, instance=None, value=None, *args, **kwargs):
		self.instance = instance
		self.value = value

	def __str__(self):
		return "Item not found: <{}: {}>".format(self.instance, self.value)


class ValidationException(ModelException):
	def __init__(self, instance=None, msg=None, *args, **kwargs):
		self.instance = instance
		self.msg = msg

	def __str__(self):
		return "Validation Error: <{}>: {}".format(self.instance, self.msg)


class MongoModel(AsyncIOMotorCollection):

	def __init__(self, db, collection=None):
		self.db = db
		self.collection = db[collection] if collection else db[type(self).__name__]

	async def get(self, id):
		item = await self.collection.find_one({'_id': id})
		if not item:
			raise NotFoundItem(type(self).__name__, id)
		return item

	async def insert(self, item):
		id = get_uniq_name()
		item['_id'] = id
		while True:
			try:
				await self.get(id)
			except NotFoundItem:
				return await self.collection.insert_one(item)
			else:
				await self.insert(item)


class Users(MongoModel):

	async def get_by_session_id(self, session_id):
		user = await self.collection.find_one({'session_id': session_id})
		if user:
			return user
		raise NotFoundItem(type(self).__name__, "session_id: " + session_id)



class Rooms(MongoModel):

	async def authenticate(self, id, password=None):
		room = await self.get(id)
		if password == room.get('password', None):
			return room
		return False


class Messages(MongoModel):

	async def get_by_room_id(self, room_id):
		length = await self.collection.count({'room_id': room_id})
		return await self.collection.find({'room_id': room_id}).to_list(length)

	async def insert(self, msg):
		return await super().insert(msg)


class Members(MongoModel):

	async def _validate_name(self, name):
		if len(name) > 30:
			raise ValidationException(
				type(self).__name__, f"Too long name: {len(name)}"
			)

	async def uniq_name(self, name, room_id):
		return not await self.collection.find_one({
			'room_id': room_id,
			'name': name
		})


	async def change_name(self, room_id, user_id, new_name):
		self._validate_name(new_name)
		return await self.collection.update_one(
			{
				'room_id': room_id,
				'user_id': user_id
			},

			{
				'$set': {
					'name': new_name
				}
			}
		)


class ChatRoom():

	def __init__(self, id, db=None):
		self.__room = []
		self.id = id
		self._db = db

	def __iter__(self):
		return iter(self.__room)

	def __contains__(self, item):
		return item in self.__room

	def __bool__(self):
		return len(self.__room)

	def __str__(self):
		return "<Room id={} len={}>".format(self.id, len(self.__room))

	def subscribe(self, ws):
		self.__room.append(ws)

	async def broadcast(self, msg):
		msg['date_time'] = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
		for ws in self:
			await ws.send_json(msg)
		
		if self._db:
			msg['room_id'] = self.id
			await Messages(self._db).insert(msg)


	def remove(self, ws):
		return self.__room.remove(ws)


if __name__ == '__main__':
	pass
