from enum import Enum


class GetClientListResponse200ItemObject(str, Enum):
    CLIENT = "client"

    def __str__(self) -> str:
        return str(self.value)
