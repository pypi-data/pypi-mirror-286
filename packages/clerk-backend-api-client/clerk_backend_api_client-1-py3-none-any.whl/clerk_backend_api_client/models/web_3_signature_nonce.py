from enum import Enum


class Web3SignatureNonce(str, Enum):
    NONCE = "nonce"

    def __str__(self) -> str:
        return str(self.value)
