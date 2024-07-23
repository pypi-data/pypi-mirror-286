from enum import Enum


class CreateRedirectURLResponse200Object(str, Enum):
    REDIRECT_URL = "redirect_url"

    def __str__(self) -> str:
        return str(self.value)
