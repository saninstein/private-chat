import sys
from aiohttp.web import Application
from aiohttp import web
import aiohttp_jinja2
from jinja2 import FileSystemLoader
import aiohttp_session
from settings import PATH, TEMPLATES_DIR
from middlewares import middlewares
from routes import routes

sys.path.append(PATH)

app = Application(middlewares=middlewares)

aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())
aiohttp_jinja2.setup(app, loader=FileSystemLoader(TEMPLATES_DIR))

for route in routes:
	app.router.add_route(*route[1:], name=route[0])

web.run_app(app, host='127.0.0.10', port=80)
