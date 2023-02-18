import logging
from logging import getLogger

from aiohttp import web

from server.api.routes import setup_routes
from server.ctx import CTXManager
from server.utils.app import on_startup


app = web.Application()
logging.basicConfig(level=logging.INFO)
app.logger = getLogger()
app.ctx = CTXManager(app)
setup_routes(app)

app['background_futures'] = [
    app.ctx.wisdom_manager.start_periodic_mailing(),
]
app.on_startup.append(on_startup)

if __name__ == '__main__':
    web.run_app(app, port=8000)
