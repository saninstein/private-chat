
middlewares = []


def middleware(middleware):
	def wrapper():
		middlewares.append(middleware)
	return wrapper()


@middleware
async def middleware_factory(app, handler):
	async def middleware_handler(request):
		print(request.url)
		return await handler(request)
	return middleware_handler
