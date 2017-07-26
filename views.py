from aiohttp.web import Response
from settings import PATH

async def index(req):
	return Response(text=PATH)
