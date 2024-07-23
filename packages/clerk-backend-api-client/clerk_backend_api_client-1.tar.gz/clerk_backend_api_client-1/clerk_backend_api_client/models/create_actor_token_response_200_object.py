from enum import Enum


class CreateActorTokenResponse200Object(str, Enum):
    ACTOR_TOKEN = "actor_token"

    def __str__(self) -> str:
        return str(self.value)
