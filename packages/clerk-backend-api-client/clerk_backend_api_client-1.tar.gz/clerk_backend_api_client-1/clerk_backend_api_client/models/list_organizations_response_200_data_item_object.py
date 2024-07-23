from enum import Enum


class ListOrganizationsResponse200DataItemObject(str, Enum):
    ORGANIZATION = "organization"

    def __str__(self) -> str:
        return str(self.value)
