from enum import Enum


class UpdateDomainResponse200Object(str, Enum):
    DOMAIN = "domain"

    def __str__(self) -> str:
        return str(self.value)
