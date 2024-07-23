from enum import Enum


class GetUserListResponse200ItemEmailAddressesItemVerificationType3Type2Strategy(str, Enum):
    FROM_OAUTH_GOOGLE = "from_oauth_google"
    OAUTH_CUSTOM_MOCK = "oauth_custom_mock"
    OAUTH_GOOGLE = "oauth_google"
    OAUTH_MOCK = "oauth_mock"

    def __str__(self) -> str:
        return str(self.value)
