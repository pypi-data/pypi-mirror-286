from enum import Enum


class UpdateOrganizationMembershipMetadataResponse200OrganizationObject(str, Enum):
    ORGANIZATION = "organization"

    def __str__(self) -> str:
        return str(self.value)
