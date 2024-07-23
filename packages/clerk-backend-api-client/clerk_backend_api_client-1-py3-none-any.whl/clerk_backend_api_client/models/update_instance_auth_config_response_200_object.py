from enum import Enum


class UpdateInstanceAuthConfigResponse200Object(str, Enum):
    INSTANCE_SETTINGS = "instance_settings"

    def __str__(self) -> str:
        return str(self.value)
