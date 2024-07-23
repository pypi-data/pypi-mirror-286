from enum import Enum


class Web3SignatureStatus(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
