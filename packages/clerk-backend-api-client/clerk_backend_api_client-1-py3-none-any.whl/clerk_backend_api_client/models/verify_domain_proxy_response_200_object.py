from enum import Enum


class VerifyDomainProxyResponse200Object(str, Enum):
    PROXY_CHECK = "proxy_check"

    def __str__(self) -> str:
        return str(self.value)
