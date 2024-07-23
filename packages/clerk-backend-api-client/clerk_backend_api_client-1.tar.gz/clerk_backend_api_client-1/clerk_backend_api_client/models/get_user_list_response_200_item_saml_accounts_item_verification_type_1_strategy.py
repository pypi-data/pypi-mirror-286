from enum import Enum


class GetUserListResponse200ItemSamlAccountsItemVerificationType1Strategy(str, Enum):
    TICKET = "ticket"

    def __str__(self) -> str:
        return str(self.value)
