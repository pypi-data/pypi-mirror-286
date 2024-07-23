from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.unlock_user_response_200_saml_accounts_item_verification_type_3_type_0_status import (
    UnlockUserResponse200SamlAccountsItemVerificationType3Type0Status,
)
from ..models.unlock_user_response_200_saml_accounts_item_verification_type_3_type_0_strategy import (
    UnlockUserResponse200SamlAccountsItemVerificationType3Type0Strategy,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.unlock_user_response_200_saml_accounts_item_verification_type_3_type_0_error_type_0 import (
        UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType0,
    )
    from ..models.unlock_user_response_200_saml_accounts_item_verification_type_3_type_0_error_type_1_type_0 import (
        UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType1Type0,
    )
    from ..models.unlock_user_response_200_saml_accounts_item_verification_type_3_type_0_error_type_2_type_0 import (
        UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType2Type0,
    )


T = TypeVar("T", bound="UnlockUserResponse200SamlAccountsItemVerificationType3Type0")


@_attrs_define
class UnlockUserResponse200SamlAccountsItemVerificationType3Type0:
    """
    Attributes:
        status (UnlockUserResponse200SamlAccountsItemVerificationType3Type0Status):
        strategy (UnlockUserResponse200SamlAccountsItemVerificationType3Type0Strategy):
        external_verification_redirect_url (Union[None, str]):
        expire_at (int):
        error (Union['UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType0',
            'UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType1Type0',
            'UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType2Type0', Unset]):
        attempts (Union[None, Unset, int]):
    """

    status: UnlockUserResponse200SamlAccountsItemVerificationType3Type0Status
    strategy: UnlockUserResponse200SamlAccountsItemVerificationType3Type0Strategy
    external_verification_redirect_url: Union[None, str]
    expire_at: int
    error: Union[
        "UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType0",
        "UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType1Type0",
        "UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType2Type0",
        Unset,
    ] = UNSET
    attempts: Union[None, Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.unlock_user_response_200_saml_accounts_item_verification_type_3_type_0_error_type_0 import (
            UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType0,
        )
        from ..models.unlock_user_response_200_saml_accounts_item_verification_type_3_type_0_error_type_1_type_0 import (
            UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType1Type0,
        )

        status = self.status.value

        strategy = self.strategy.value

        external_verification_redirect_url: Union[None, str]
        external_verification_redirect_url = self.external_verification_redirect_url

        expire_at = self.expire_at

        error: Union[Dict[str, Any], Unset]
        if isinstance(self.error, Unset):
            error = UNSET
        elif isinstance(self.error, UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType0):
            error = self.error.to_dict()
        elif isinstance(self.error, UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType1Type0):
            error = self.error.to_dict()
        else:
            error = self.error.to_dict()

        attempts: Union[None, Unset, int]
        if isinstance(self.attempts, Unset):
            attempts = UNSET
        else:
            attempts = self.attempts

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "status": status,
                "strategy": strategy,
                "external_verification_redirect_url": external_verification_redirect_url,
                "expire_at": expire_at,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if attempts is not UNSET:
            field_dict["attempts"] = attempts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.unlock_user_response_200_saml_accounts_item_verification_type_3_type_0_error_type_0 import (
            UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType0,
        )
        from ..models.unlock_user_response_200_saml_accounts_item_verification_type_3_type_0_error_type_1_type_0 import (
            UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType1Type0,
        )
        from ..models.unlock_user_response_200_saml_accounts_item_verification_type_3_type_0_error_type_2_type_0 import (
            UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType2Type0,
        )

        d = src_dict.copy()
        status = UnlockUserResponse200SamlAccountsItemVerificationType3Type0Status(d.pop("status"))

        strategy = UnlockUserResponse200SamlAccountsItemVerificationType3Type0Strategy(d.pop("strategy"))

        def _parse_external_verification_redirect_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        external_verification_redirect_url = _parse_external_verification_redirect_url(
            d.pop("external_verification_redirect_url")
        )

        expire_at = d.pop("expire_at")

        def _parse_error(
            data: object,
        ) -> Union[
            "UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType0",
            "UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType1Type0",
            "UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType2Type0",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType0.from_dict(data)

                return error_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_1_type_0 = (
                    UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType1Type0.from_dict(data)
                )

                return error_type_1_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            error_type_2_type_0 = UnlockUserResponse200SamlAccountsItemVerificationType3Type0ErrorType2Type0.from_dict(
                data
            )

            return error_type_2_type_0

        error = _parse_error(d.pop("error", UNSET))

        def _parse_attempts(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        attempts = _parse_attempts(d.pop("attempts", UNSET))

        unlock_user_response_200_saml_accounts_item_verification_type_3_type_0 = cls(
            status=status,
            strategy=strategy,
            external_verification_redirect_url=external_verification_redirect_url,
            expire_at=expire_at,
            error=error,
            attempts=attempts,
        )

        return unlock_user_response_200_saml_accounts_item_verification_type_3_type_0
