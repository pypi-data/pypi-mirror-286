from enum import Enum


class LockUserResponse200SamlAccountsItemVerificationType1Strategy(str, Enum):
    TICKET = "ticket"

    def __str__(self) -> str:
        return str(self.value)
