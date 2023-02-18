import typing

if typing.TYPE_CHECKING:
    from server.ctx import CTXManager


class BaseCTX:
    class Meta:
        name = "base_context"

    def __init__(self, ctx: "CTXManager"):
        self.app = ctx.app
        self.ctx = ctx
        self.logger = ctx.app.logger.getChild(self.Meta.name)
        self._init_()

    def _init_(self) -> None:
        return None


class BaseManager(BaseCTX):
    class Meta:
        name = "base_manager"
