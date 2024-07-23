from enum import Enum


class CreateUserResponse200SamlAccountsItemVerificationType2Type1Strategy(str, Enum):
    TICKET = "ticket"

    def __str__(self) -> str:
        return str(self.value)
