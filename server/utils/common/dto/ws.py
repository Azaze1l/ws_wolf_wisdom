import typing
from asyncio import Task
from dataclasses import dataclass

from aiohttp.web_ws import WebSocketResponse


@dataclass
class Connection:
    session: WebSocketResponse
    timeout_task: Task
    close_callback: typing.Callable[[str], typing.Awaitable] | None


@dataclass
class Event:
    type: str
    payload: dict

    def __str__(self):
        return f"Event<{self.type}>"
