from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.update_phone_number_response_200_verification_type_2_type_0_status import (
    UpdatePhoneNumberResponse200VerificationType2Type0Status,
)
from ..models.update_phone_number_response_200_verification_type_2_type_0_strategy import (
    UpdatePhoneNumberResponse200VerificationType2Type0Strategy,
)

T = TypeVar("T", bound="UpdatePhoneNumberResponse200VerificationType2Type0")


@_attrs_define
class UpdatePhoneNumberResponse200VerificationType2Type0:
    """
    Attributes:
        status (UpdatePhoneNumberResponse200VerificationType2Type0Status):
        strategy (UpdatePhoneNumberResponse200VerificationType2Type0Strategy):
        attempts (int):
        expire_at (int):
    """

    status: UpdatePhoneNumberResponse200VerificationType2Type0Status
    strategy: UpdatePhoneNumberResponse200VerificationType2Type0Strategy
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
        status = UpdatePhoneNumberResponse200VerificationType2Type0Status(d.pop("status"))

        strategy = UpdatePhoneNumberResponse200VerificationType2Type0Strategy(d.pop("strategy"))

        attempts = d.pop("attempts")

        expire_at = d.pop("expire_at")

        update_phone_number_response_200_verification_type_2_type_0 = cls(
            status=status,
            strategy=strategy,
            attempts=attempts,
            expire_at=expire_at,
        )

        return update_phone_number_response_200_verification_type_2_type_0
