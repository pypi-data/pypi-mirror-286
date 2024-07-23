from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.update_email_address_response_200_verification_type_0_status import (
    UpdateEmailAddressResponse200VerificationType0Status,
)
from ..models.update_email_address_response_200_verification_type_0_strategy import (
    UpdateEmailAddressResponse200VerificationType0Strategy,
)

T = TypeVar("T", bound="UpdateEmailAddressResponse200VerificationType0")


@_attrs_define
class UpdateEmailAddressResponse200VerificationType0:
    """
    Attributes:
        status (UpdateEmailAddressResponse200VerificationType0Status):
        strategy (UpdateEmailAddressResponse200VerificationType0Strategy):
        attempts (int):
        expire_at (int):
    """

    status: UpdateEmailAddressResponse200VerificationType0Status
    strategy: UpdateEmailAddressResponse200VerificationType0Strategy
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
        status = UpdateEmailAddressResponse200VerificationType0Status(d.pop("status"))

        strategy = UpdateEmailAddressResponse200VerificationType0Strategy(d.pop("strategy"))

        attempts = d.pop("attempts")

        expire_at = d.pop("expire_at")

        update_email_address_response_200_verification_type_0 = cls(
            status=status,
            strategy=strategy,
            attempts=attempts,
            expire_at=expire_at,
        )

        return update_email_address_response_200_verification_type_0
