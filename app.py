import sys
import asyncio
from aiohttp.web import Application
from aiohttp import web
import aiohttp_jinja2
from jinja2 import FileSystemLoader
import aiohttp_session
from settings import PATH, TEMPLATES_DIR, DEBUG, MONGO_IP, MONGO_PORT
from middlewares import middlewares
from motor.motor_asyncio import AsyncIOMotorClient
from routes import routes


async def on_shutdown(app):
	for ws in app.wss:
		await ws.close(code=1001, message='Server shutdown')


async def static_processor(req):
	return {'STATIC_URL': '/static'}


sys.path.append(PATH)


def get_app():
	app = Application(middlewares=middlewares)
	app.on_shutdown.append(on_shutdown)

	app.client = AsyncIOMotorClient(MONGO_IP, MONGO_PORT)
	app.rooms = []

	aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())
	aiohttp_jinja2.setup(
		app,
		loader=FileSystemLoader(TEMPLATES_DIR),
		context_processors=[static_processor]
	)

	for route in routes:
		app.router.add_route(*route[1:], name=route[0])
	app.router.add_static('/static', 'static', name='static')
	return app


if __name__ == "__main__":
	app = get_app()
	web.run_app(app, host='127.0.0.1', port=80)







