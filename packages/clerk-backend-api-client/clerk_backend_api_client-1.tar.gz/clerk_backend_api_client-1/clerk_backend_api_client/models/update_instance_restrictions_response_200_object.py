from enum import Enum


class UpdateInstanceRestrictionsResponse200Object(str, Enum):
    INSTANCE_RESTRICTIONS = "instance_restrictions"

    def __str__(self) -> str:
        return str(self.value)
