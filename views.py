from aiohttp import web, WSMsgType
from settings import PATH
from datetime import datetime
from models import Rooms, ChatRoom
import aiohttp_jinja2


@aiohttp_jinja2.template('chat/index.html')
async def index(req):
	return {'room': req.match_info.get('room')}


async def create_room(req):
	room = await Rooms(req.db).insert({})
	req.app.rooms.append(ChatRoom(room.inserted_id, req.db))
	return web.HTTPFound('/')


@aiohttp_jinja2.template('chats/index.html')
async def rooms(req):
	rooms = []
	async for room in Rooms(req.db).collection.find({}, {'_id': 1}):
		rooms.append(room.get('_id'))
	print(rooms)
	return {'rooms': rooms}


class WebSocket(web.View):
	async def get(self):
		ws = web.WebSocketResponse()
		await ws.prepare(self.request)
		room = [x for x in self.request.app.rooms if x.id == self.request.match_info['room']]
		if len(room) != 1:
			room = [ChatRoom(self.request.match_info['room'], self.request.db)]
		room = room[0]
		room.subscribe(ws)
		async for msg in ws:
			print("Message: ", msg.data)
			if msg.type == WSMsgType.TEXT:
				if msg.data == 'close':
					await ws.close()
				else:
					await room.broadcast({
						'msg': msg.data,
					})
			elif msg.type == WSMsgType.ERROR:
				print('Ws closed with E: %' % ws.exception())
		room.remove(ws)
		print('WS Closed')
		return ws
