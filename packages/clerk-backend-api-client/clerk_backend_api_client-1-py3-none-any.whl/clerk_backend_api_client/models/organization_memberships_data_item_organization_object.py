from enum import Enum


class OrganizationMembershipsDataItemOrganizationObject(str, Enum):
    ORGANIZATION = "organization"

    def __str__(self) -> str:
        return str(self.value)
