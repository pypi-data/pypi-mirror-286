from enum import Enum


class UpdateUserResponse200SamlAccountsItemVerificationType3Type1Strategy(str, Enum):
    TICKET = "ticket"

    def __str__(self) -> str:
        return str(self.value)
