from enum import Enum


class CreateOrganizationResponse200Object(str, Enum):
    ORGANIZATION = "organization"

    def __str__(self) -> str:
        return str(self.value)
