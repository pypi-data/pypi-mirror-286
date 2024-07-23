from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.delete_user_profile_image_response_200_phone_numbers_item_verification_type_0_status import (
    DeleteUserProfileImageResponse200PhoneNumbersItemVerificationType0Status,
)
from ..models.delete_user_profile_image_response_200_phone_numbers_item_verification_type_0_strategy import (
    DeleteUserProfileImageResponse200PhoneNumbersItemVerificationType0Strategy,
)

T = TypeVar("T", bound="DeleteUserProfileImageResponse200PhoneNumbersItemVerificationType0")


@_attrs_define
class DeleteUserProfileImageResponse200PhoneNumbersItemVerificationType0:
    """
    Attributes:
        status (DeleteUserProfileImageResponse200PhoneNumbersItemVerificationType0Status):
        strategy (DeleteUserProfileImageResponse200PhoneNumbersItemVerificationType0Strategy):
        attempts (int):
        expire_at (int):
    """

    status: DeleteUserProfileImageResponse200PhoneNumbersItemVerificationType0Status
    strategy: DeleteUserProfileImageResponse200PhoneNumbersItemVerificationType0Strategy
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
        status = DeleteUserProfileImageResponse200PhoneNumbersItemVerificationType0Status(d.pop("status"))

        strategy = DeleteUserProfileImageResponse200PhoneNumbersItemVerificationType0Strategy(d.pop("strategy"))

        attempts = d.pop("attempts")

        expire_at = d.pop("expire_at")

        delete_user_profile_image_response_200_phone_numbers_item_verification_type_0 = cls(
            status=status,
            strategy=strategy,
            attempts=attempts,
            expire_at=expire_at,
        )

        return delete_user_profile_image_response_200_phone_numbers_item_verification_type_0
