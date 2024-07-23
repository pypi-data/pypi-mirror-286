from enum import Enum


class GetUsersCountResponse200Object(str, Enum):
    TOTAL_COUNT = "total_count"

    def __str__(self) -> str:
        return str(self.value)
