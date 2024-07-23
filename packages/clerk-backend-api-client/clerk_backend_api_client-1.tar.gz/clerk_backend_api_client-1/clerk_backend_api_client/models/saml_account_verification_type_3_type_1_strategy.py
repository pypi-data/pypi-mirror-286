from enum import Enum


class SAMLAccountVerificationType3Type1Strategy(str, Enum):
    TICKET = "ticket"

    def __str__(self) -> str:
        return str(self.value)
