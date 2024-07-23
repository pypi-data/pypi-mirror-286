from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_3_type_0_status import (
    DeleteUserProfileImageResponse200EmailAddressesItemVerificationType3Type0Status,
)
from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_3_type_0_strategy import (
    DeleteUserProfileImageResponse200EmailAddressesItemVerificationType3Type0Strategy,
)

T = TypeVar("T", bound="DeleteUserProfileImageResponse200EmailAddressesItemVerificationType3Type0")


@_attrs_define
class DeleteUserProfileImageResponse200EmailAddressesItemVerificationType3Type0:
    """
    Attributes:
        status (DeleteUserProfileImageResponse200EmailAddressesItemVerificationType3Type0Status):
        strategy (DeleteUserProfileImageResponse200EmailAddressesItemVerificationType3Type0Strategy):
        attempts (int):
        expire_at (int):
    """

    status: DeleteUserProfileImageResponse200EmailAddressesItemVerificationType3Type0Status
    strategy: DeleteUserProfileImageResponse200EmailAddressesItemVerificationType3Type0Strategy
    attempts: int
    expire_at: int

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        strategy = self.strategy.value

        attempts = self.attempts

        expire_at = self.expire_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "status": status,
                "strategy": strategy,
                "attempts": attempts,
                "expire_at": expire_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = DeleteUserProfileImageResponse200EmailAddressesItemVerificationType3Type0Status(d.pop("status"))

        strategy = DeleteUserProfileImageResponse200EmailAddressesItemVerificationType3Type0Strategy(d.pop("strategy"))

        attempts = d.pop("attempts")

        expire_at = d.pop("expire_at")

        delete_user_profile_image_response_200_email_addresses_item_verification_type_3_type_0 = cls(
            status=status,
            strategy=strategy,
            attempts=attempts,
            expire_at=expire_at,
        )

        return delete_user_profile_image_response_200_email_addresses_item_verification_type_3_type_0
