from enum import Enum


class CreateOrganizationMembershipResponse200OrganizationObject(str, Enum):
    ORGANIZATION = "organization"

    def __str__(self) -> str:
        return str(self.value)
