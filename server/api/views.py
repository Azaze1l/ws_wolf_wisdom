import os

from aiohttp import web

from server import BASE_DIR
from server.base.application import View
from server.ctx.ws.ws_ctx import WSContextManager


class IndexView(View):
    async def get(self):
        with open(os.path.join(BASE_DIR, "client", "index.html"), "r") as f:
            file = f.read()

        return web.Response(
            body=file,
            headers={
                "Content-Type": "text/html",
            },
        )


class WSConnectView(View):
    async def get(self):
        async with WSContextManager(
            ctx=self.ctx.ws_ctx,
            request=self.request,
            close_callback=self.ctx.wisdom_manager.on_user_disconnect,
        ) as connection_id:
            await self.ctx.wisdom_manager.handle(connection_id)
        return
