from server.base.context import BaseCTX
from server.utils.common.dto import User


class UsersCtx(BaseCTX):
    def _init_(self) -> None:
        self._users: dict[str, User] = {}

    async def list_users(self) -> list[User]:
        return list(self._users.values())

    async def add(
        self,
        _id: str,
    ) -> User:
        user = User(
            id=_id,
            subscribed=False,
        )
        self._users[_id] = user
        return user

    async def updated_subscription_status(self, _id: str, sub_status: bool) -> None:
        self._users[_id].subscribed = sub_status

    async def remove(self, _id: str) -> None:
        self._users.pop(_id)

    async def get(self, _id: str) -> User:
        return self._users[_id]
