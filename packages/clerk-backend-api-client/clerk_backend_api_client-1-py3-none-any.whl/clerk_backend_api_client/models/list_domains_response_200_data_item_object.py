from enum import Enum


class ListDomainsResponse200DataItemObject(str, Enum):
    DOMAIN = "domain"

    def __str__(self) -> str:
        return str(self.value)
