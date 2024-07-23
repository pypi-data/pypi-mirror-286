from enum import Enum


class UserSamlAccountsItemVerificationType2Type1Strategy(str, Enum):
    TICKET = "ticket"

    def __str__(self) -> str:
        return str(self.value)
