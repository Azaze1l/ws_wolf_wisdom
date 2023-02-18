from logging import Logger

from aiohttp import web

from server.ctx import CTXManager


class Application(web.Application):
    ctx: CTXManager
    logger: Logger


class Request(web.Request):
    user_id: str

    @property
    def app(self) -> Application:
        return super().app


class View(web.View):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def app(self) -> "Application":
        return self.request.app

    @property
    def ctx(self) -> CTXManager:
        return self.app.ctx
