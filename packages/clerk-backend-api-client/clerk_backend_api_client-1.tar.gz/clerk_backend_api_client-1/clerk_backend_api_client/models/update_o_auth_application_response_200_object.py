from enum import Enum


class UpdateOAuthApplicationResponse200Object(str, Enum):
    OAUTH_APPLICATION = "oauth_application"

    def __str__(self) -> str:
        return str(self.value)
