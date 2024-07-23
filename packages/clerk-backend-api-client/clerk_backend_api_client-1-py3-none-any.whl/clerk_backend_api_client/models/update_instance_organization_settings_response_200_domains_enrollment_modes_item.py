from enum import Enum


class UpdateInstanceOrganizationSettingsResponse200DomainsEnrollmentModesItem(str, Enum):
    AUTOMATIC_INVITATION = "automatic_invitation"
    AUTOMATIC_SUGGESTION = "automatic_suggestion"
    MANUAL_INVITATION = "manual_invitation"

    def __str__(self) -> str:
        return str(self.value)
