from enum import Enum


class ListJWTTemplatesResponse200ItemObject(str, Enum):
    JWT_TEMPLATE = "jwt_template"

    def __str__(self) -> str:
        return str(self.value)
