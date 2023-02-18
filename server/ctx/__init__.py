import typing

from server.ctx.users.users_ctx import UsersCtx
from server.ctx.wolf_wisdom.wisdom_ctx import WisdomManager
from server.ctx.ws.ws_ctx import WSCtx

if typing.TYPE_CHECKING:
    from server.base.application import Application


class CTXManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.ws_ctx = WSCtx(self)
        self.users_ctx = UsersCtx(self)
        self.wisdom_manager = WisdomManager(self)
