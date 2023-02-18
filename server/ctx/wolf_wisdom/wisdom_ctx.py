import json
import os
import random
from asyncio import sleep

from server import BASE_DIR
from server.base.context import BaseManager
from server.utils.common.dto import Event


class ServerEventType:
    INITIAL = "initial"
    SUBSCRIBE_CONFIRMATION = "subscribe_confirmation"
    WISDOM_DISTRIBUTION = "wisdom_distribution"


class ClientEventType:
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    PING = "ping"


class WisdomManager(BaseManager):
    class Meta:
        name = "wisdom_manager"

    async def handle(self, connection_id: str):
        await self._send_initial_event(connection_id)
        async for event in self.ctx.ws_ctx.stream(connection_id):
            should_continue = await self._handle_event(event, connection_id)
            if not should_continue:
                break

    async def _handle_event(self, event: Event, connection_id: str) -> bool:
        match event.type:
            case ClientEventType.PING:
                return True
            case ClientEventType.CONNECT:
                user = await self.ctx.users_ctx.add(
                    _id=connection_id,
                )
                self.logger.info(f"New user connected: {user}")
                return True

            case ClientEventType.DISCONNECT:
                self.logger.info(f"User {connection_id} disconnected")
                await self.on_user_disconnect(connection_id)
                return True

            case ClientEventType.SUBSCRIBE:
                self.logger.info(f"User {connection_id}'ve been subscribed")
                await self.ctx.users_ctx.updated_subscription_status(
                    _id=connection_id, sub_status=True
                )
                await self.ctx.ws_ctx.push(
                    Event(
                        type=ServerEventType.SUBSCRIBE_CONFIRMATION,
                        payload={"status": "ok"},
                    ),
                    connection_id=connection_id,
                )
                return True

            case ClientEventType.UNSUBSCRIBE:
                self.logger.info(f"User {connection_id}'ve been unsubscribed")
                await self.ctx.users_ctx.updated_subscription_status(
                    _id=connection_id, sub_status=False
                )
                return True
            case _:
                raise NotImplementedError

    async def _send_initial_event(self, connection_id: str):
        event = Event(
            type=ServerEventType.INITIAL,
            payload={"id": connection_id},
        )
        await self.ctx.ws_ctx.push(event, connection_id=connection_id)

    async def on_user_disconnect(self, connection_id: str) -> None:
        await self.ctx.users_ctx.remove(connection_id)

    async def start_periodic_mailing(self):
        with open(
            os.path.join(BASE_DIR, "assets", "wolf_wisdom.json"), "r", encoding="utf-8"
        ) as f:
            quotes = json.load(f)["quotes"]

        while True:
            try:
                await self.ctx.ws_ctx.broadcast(
                    event=Event(
                        type=ServerEventType.WISDOM_DISTRIBUTION,
                        payload={"message": random.choice(quotes)},
                    ),
                    except_of=[
                        user.id
                        for user in await self.ctx.users_ctx.list_users()
                        if user.subscribed is False
                    ],
                )
                await sleep(10)
            except Exception:  # noqa
                pass
