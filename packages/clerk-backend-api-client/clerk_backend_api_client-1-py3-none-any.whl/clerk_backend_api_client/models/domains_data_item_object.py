from enum import Enum


class DomainsDataItemObject(str, Enum):
    DOMAIN = "domain"

    def __str__(self) -> str:
        return str(self.value)
