from enum import Enum


class SchemasPasskeyVerificationType2Type0Nonce(str, Enum):
    NONCE = "nonce"

    def __str__(self) -> str:
        return str(self.value)
