from enum import Enum


class UpdateJWTTemplateResponse200Object(str, Enum):
    JWT_TEMPLATE = "jwt_template"

    def __str__(self) -> str:
        return str(self.value)
