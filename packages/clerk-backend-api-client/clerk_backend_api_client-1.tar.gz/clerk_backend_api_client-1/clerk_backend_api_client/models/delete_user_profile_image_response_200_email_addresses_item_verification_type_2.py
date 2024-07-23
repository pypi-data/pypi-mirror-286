from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_2_status import (
    DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2Status,
)
from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_2_strategy import (
    DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2Strategy,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_2_error_type_0 import (
        DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType0,
    )
    from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_2_error_type_1_type_0 import (
        DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType1Type0,
    )
    from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_2_error_type_2_type_0 import (
        DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType2Type0,
    )


T = TypeVar("T", bound="DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2")


@_attrs_define
class DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2:
    """
    Attributes:
        status (DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2Status):
        strategy (DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2Strategy):
        expire_at (int):
        external_verification_redirect_url (Union[Unset, str]):
        error (Union['DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType0',
            'DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType1Type0',
            'DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType2Type0', Unset]):
        attempts (Union[None, Unset, int]):
    """

    status: DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2Status
    strategy: DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2Strategy
    expire_at: int
    external_verification_redirect_url: Union[Unset, str] = UNSET
    error: Union[
        "DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType0",
        "DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType1Type0",
        "DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType2Type0",
        Unset,
    ] = UNSET
    attempts: Union[None, Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_2_error_type_0 import (
            DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType0,
        )
        from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_2_error_type_1_type_0 import (
            DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType1Type0,
        )

        status = self.status.value

        strategy = self.strategy.value

        expire_at = self.expire_at

        external_verification_redirect_url = self.external_verification_redirect_url

        error: Union[Dict[str, Any], Unset]
        if isinstance(self.error, Unset):
            error = UNSET
        elif isinstance(self.error, DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType0):
            error = self.error.to_dict()
        elif isinstance(
            self.error, DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType1Type0
        ):
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
                "expire_at": expire_at,
            }
        )
        if external_verification_redirect_url is not UNSET:
            field_dict["external_verification_redirect_url"] = external_verification_redirect_url
        if error is not UNSET:
            field_dict["error"] = error
        if attempts is not UNSET:
            field_dict["attempts"] = attempts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_2_error_type_0 import (
            DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType0,
        )
        from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_2_error_type_1_type_0 import (
            DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType1Type0,
        )
        from ..models.delete_user_profile_image_response_200_email_addresses_item_verification_type_2_error_type_2_type_0 import (
            DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType2Type0,
        )

        d = src_dict.copy()
        status = DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2Status(d.pop("status"))

        strategy = DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2Strategy(d.pop("strategy"))

        expire_at = d.pop("expire_at")

        external_verification_redirect_url = d.pop("external_verification_redirect_url", UNSET)

        def _parse_error(
            data: object,
        ) -> Union[
            "DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType0",
            "DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType1Type0",
            "DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType2Type0",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType0.from_dict(
                    data
                )

                return error_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_1_type_0 = (
                    DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType1Type0.from_dict(data)
                )

                return error_type_1_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            error_type_2_type_0 = (
                DeleteUserProfileImageResponse200EmailAddressesItemVerificationType2ErrorType2Type0.from_dict(data)
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

        delete_user_profile_image_response_200_email_addresses_item_verification_type_2 = cls(
            status=status,
            strategy=strategy,
            expire_at=expire_at,
            external_verification_redirect_url=external_verification_redirect_url,
            error=error,
            attempts=attempts,
        )

        return delete_user_profile_image_response_200_email_addresses_item_verification_type_2
