from dataclasses import dataclass


@dataclass
class User:
    id: str
    subscribed: bool

    def __str__(self):
        return f"User {self.id}; subscribed={self.subscribed}"
