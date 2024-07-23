from enum import Enum


class Web3WalletVerificationType0Strategy(str, Enum):
    WEB3_METAMASK_SIGNATURE = "web3_metamask_signature"

    def __str__(self) -> str:
        return str(self.value)
