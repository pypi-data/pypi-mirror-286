from enum import Enum


class ListOrganizationMembershipsResponse200DataItemObject(str, Enum):
    ORGANIZATION_MEMBERSHIP = "organization_membership"

    def __str__(self) -> str:
        return str(self.value)
