from enum import Enum


class GetUserListResponse200ItemWeb3WalletsItemObject(str, Enum):
    WEB3_WALLET = "web3_wallet"

    def __str__(self) -> str:
        return str(self.value)
