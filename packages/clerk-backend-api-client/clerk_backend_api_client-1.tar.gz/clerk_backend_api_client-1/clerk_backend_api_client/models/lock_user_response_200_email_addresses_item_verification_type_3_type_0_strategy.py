from enum import Enum


class LockUserResponse200EmailAddressesItemVerificationType3Type0Strategy(str, Enum):
    EMAIL_CODE = "email_code"
    PHONE_CODE = "phone_code"
    RESET_PASSWORD_EMAIL_CODE = "reset_password_email_code"

    def __str__(self) -> str:
        return str(self.value)
