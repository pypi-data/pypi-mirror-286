from enum import Enum


class ListOrganizationMembershipsResponse200DataItemOrganizationObject(str, Enum):
    ORGANIZATION = "organization"

    def __str__(self) -> str:
        return str(self.value)
