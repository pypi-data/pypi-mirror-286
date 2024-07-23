from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.phone_number_verification_type_3_type_0_status import PhoneNumberVerificationType3Type0Status
from ..models.phone_number_verification_type_3_type_0_strategy import PhoneNumberVerificationType3Type0Strategy

T = TypeVar("T", bound="PhoneNumberVerificationType3Type0")


@_attrs_define
class PhoneNumberVerificationType3Type0:
    """
    Attributes:
        status (PhoneNumberVerificationType3Type0Status):
        strategy (PhoneNumberVerificationType3Type0Strategy):
        attempts (int):
        expire_at (int):
    """

    status: PhoneNumberVerificationType3Type0Status
    strategy: PhoneNumberVerificationType3Type0Strategy
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
        status = PhoneNumberVerificationType3Type0Status(d.pop("status"))

        strategy = PhoneNumberVerificationType3Type0Strategy(d.pop("strategy"))

        attempts = d.pop("attempts")

        expire_at = d.pop("expire_at")

        phone_number_verification_type_3_type_0 = cls(
            status=status,
            strategy=strategy,
            attempts=attempts,
            expire_at=expire_at,
        )

        return phone_number_verification_type_3_type_0
