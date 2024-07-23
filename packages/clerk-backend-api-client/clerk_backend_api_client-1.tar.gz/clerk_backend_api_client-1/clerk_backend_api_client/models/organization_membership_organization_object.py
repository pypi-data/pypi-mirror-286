from enum import Enum


class OrganizationMembershipOrganizationObject(str, Enum):
    ORGANIZATION = "organization"

    def __str__(self) -> str:
        return str(self.value)
