from datetime import datetime
import time


middlewares = []


def middleware(middleware):
	def wrapper():
		middlewares.append(middleware)
	return wrapper()


@middleware
async def middleware_factory(app, handler):
	async def middleware_handler(request):
		before_time = time.time()
		response = await handler(request)
		print('[{}] {} {} {} {}'.format(datetime.now(), response.status, request.method, request.url, round(time.time() - before_time, 4)))
		return response

	return middleware_handler


@middleware
async def db_linked_middleware(app, handler):
	async def middleware_handler(request):
		request.db = app.client.chat_database
		return await handler(request)
	return middleware_handler
