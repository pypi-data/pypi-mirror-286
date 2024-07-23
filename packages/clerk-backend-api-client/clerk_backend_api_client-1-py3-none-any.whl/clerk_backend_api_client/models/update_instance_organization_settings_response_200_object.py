from enum import Enum


class UpdateInstanceOrganizationSettingsResponse200Object(str, Enum):
    ORGANIZATION_SETTINGS = "organization_settings"

    def __str__(self) -> str:
        return str(self.value)
