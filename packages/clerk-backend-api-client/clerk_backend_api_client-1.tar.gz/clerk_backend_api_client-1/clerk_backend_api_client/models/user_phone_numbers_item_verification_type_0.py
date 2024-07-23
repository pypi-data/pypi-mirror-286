from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.user_phone_numbers_item_verification_type_0_status import UserPhoneNumbersItemVerificationType0Status
from ..models.user_phone_numbers_item_verification_type_0_strategy import UserPhoneNumbersItemVerificationType0Strategy

T = TypeVar("T", bound="UserPhoneNumbersItemVerificationType0")


@_attrs_define
class UserPhoneNumbersItemVerificationType0:
    """
    Attributes:
        status (UserPhoneNumbersItemVerificationType0Status):
        strategy (UserPhoneNumbersItemVerificationType0Strategy):
        attempts (int):
        expire_at (int):
    """

    status: UserPhoneNumbersItemVerificationType0Status
    strategy: UserPhoneNumbersItemVerificationType0Strategy
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
        status = UserPhoneNumbersItemVerificationType0Status(d.pop("status"))

        strategy = UserPhoneNumbersItemVerificationType0Strategy(d.pop("strategy"))

        attempts = d.pop("attempts")

        expire_at = d.pop("expire_at")

        user_phone_numbers_item_verification_type_0 = cls(
            status=status,
            strategy=strategy,
            attempts=attempts,
            expire_at=expire_at,
        )

        return user_phone_numbers_item_verification_type_0
