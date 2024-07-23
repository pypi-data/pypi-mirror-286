from enum import Enum


class SetUserProfileImageResponse200SamlAccountsItemVerificationType1Strategy(str, Enum):
    TICKET = "ticket"

    def __str__(self) -> str:
        return str(self.value)
