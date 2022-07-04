# nothing here to discuss

from aiohttp import web
from .stream_routes import routes
import aiohttp_jinja2 # for jinja format
import jinja2 # this is also for jinja
import os # for jinja format setup

async def web_server():
	web_app = web.Application(client_max_size=30000000)
	web_app.add_routes(routes)
	aiohttp_jinja2.setup(
    app=web_app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "zero_two_bot/server/templates"))
	)
	return web_app
