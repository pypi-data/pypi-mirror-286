from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.get_email_address_response_200_verification_type_3_type_0_status import (
    GetEmailAddressResponse200VerificationType3Type0Status,
)
from ..models.get_email_address_response_200_verification_type_3_type_0_strategy import (
    GetEmailAddressResponse200VerificationType3Type0Strategy,
)

T = TypeVar("T", bound="GetEmailAddressResponse200VerificationType3Type0")


@_attrs_define
class GetEmailAddressResponse200VerificationType3Type0:
    """
    Attributes:
        status (GetEmailAddressResponse200VerificationType3Type0Status):
        strategy (GetEmailAddressResponse200VerificationType3Type0Strategy):
        attempts (int):
        expire_at (int):
    """

    status: GetEmailAddressResponse200VerificationType3Type0Status
    strategy: GetEmailAddressResponse200VerificationType3Type0Strategy
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
        status = GetEmailAddressResponse200VerificationType3Type0Status(d.pop("status"))

        strategy = GetEmailAddressResponse200VerificationType3Type0Strategy(d.pop("strategy"))

        attempts = d.pop("attempts")

        expire_at = d.pop("expire_at")

        get_email_address_response_200_verification_type_3_type_0 = cls(
            status=status,
            strategy=strategy,
            attempts=attempts,
            expire_at=expire_at,
        )

        return get_email_address_response_200_verification_type_3_type_0
