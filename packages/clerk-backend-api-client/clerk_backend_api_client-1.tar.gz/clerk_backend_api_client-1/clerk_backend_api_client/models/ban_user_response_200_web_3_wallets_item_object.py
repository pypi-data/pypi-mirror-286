from enum import Enum


class BanUserResponse200Web3WalletsItemObject(str, Enum):
    WEB3_WALLET = "web3_wallet"

    def __str__(self) -> str:
        return str(self.value)
