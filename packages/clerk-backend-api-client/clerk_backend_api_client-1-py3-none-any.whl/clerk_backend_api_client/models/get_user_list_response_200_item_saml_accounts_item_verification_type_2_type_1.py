from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.get_user_list_response_200_item_saml_accounts_item_verification_type_2_type_1_status import (
    GetUserListResponse200ItemSamlAccountsItemVerificationType2Type1Status,
)
from ..models.get_user_list_response_200_item_saml_accounts_item_verification_type_2_type_1_strategy import (
    GetUserListResponse200ItemSamlAccountsItemVerificationType2Type1Strategy,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetUserListResponse200ItemSamlAccountsItemVerificationType2Type1")


@_attrs_define
class GetUserListResponse200ItemSamlAccountsItemVerificationType2Type1:
    """
    Attributes:
        status (GetUserListResponse200ItemSamlAccountsItemVerificationType2Type1Status):
        strategy (GetUserListResponse200ItemSamlAccountsItemVerificationType2Type1Strategy):
        attempts (Union[None, Unset, int]):
        expire_at (Union[None, Unset, int]):
    """

    status: GetUserListResponse200ItemSamlAccountsItemVerificationType2Type1Status
    strategy: GetUserListResponse200ItemSamlAccountsItemVerificationType2Type1Strategy
    attempts: Union[None, Unset, int] = UNSET
    expire_at: Union[None, Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        strategy = self.strategy.value

        attempts: Union[None, Unset, int]
        if isinstance(self.attempts, Unset):
            attempts = UNSET
        else:
            attempts = self.attempts

        expire_at: Union[None, Unset, int]
        if isinstance(self.expire_at, Unset):
            expire_at = UNSET
        else:
            expire_at = self.expire_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "status": status,
                "strategy": strategy,
            }
        )
        if attempts is not UNSET:
            field_dict["attempts"] = attempts
        if expire_at is not UNSET:
            field_dict["expire_at"] = expire_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = GetUserListResponse200ItemSamlAccountsItemVerificationType2Type1Status(d.pop("status"))

        strategy = GetUserListResponse200ItemSamlAccountsItemVerificationType2Type1Strategy(d.pop("strategy"))

        def _parse_attempts(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        attempts = _parse_attempts(d.pop("attempts", UNSET))

        def _parse_expire_at(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        expire_at = _parse_expire_at(d.pop("expire_at", UNSET))

        get_user_list_response_200_item_saml_accounts_item_verification_type_2_type_1 = cls(
            status=status,
            strategy=strategy,
            attempts=attempts,
            expire_at=expire_at,
        )

        return get_user_list_response_200_item_saml_accounts_item_verification_type_2_type_1
