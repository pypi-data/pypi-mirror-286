from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..models.unban_user_response_200_passkeys_item_object import UnbanUserResponse200PasskeysItemObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.unban_user_response_200_passkeys_item_verification_type_0 import (
        UnbanUserResponse200PasskeysItemVerificationType0,
    )
    from ..models.unban_user_response_200_passkeys_item_verification_type_1_type_0 import (
        UnbanUserResponse200PasskeysItemVerificationType1Type0,
    )
    from ..models.unban_user_response_200_passkeys_item_verification_type_2_type_0 import (
        UnbanUserResponse200PasskeysItemVerificationType2Type0,
    )


T = TypeVar("T", bound="UnbanUserResponse200PasskeysItem")


@_attrs_define
class UnbanUserResponse200PasskeysItem:
    """
    Attributes:
        object_ (UnbanUserResponse200PasskeysItemObject): String representing the object's type. Objects of the same
            type share the same value.
        name (str):
        last_used_at (int): Unix timestamp of when the passkey was last used.
        verification (Union['UnbanUserResponse200PasskeysItemVerificationType0',
            'UnbanUserResponse200PasskeysItemVerificationType1Type0',
            'UnbanUserResponse200PasskeysItemVerificationType2Type0']):
        id (Union[Unset, str]):
    """

    object_: UnbanUserResponse200PasskeysItemObject
    name: str
    last_used_at: int
    verification: Union[
        "UnbanUserResponse200PasskeysItemVerificationType0",
        "UnbanUserResponse200PasskeysItemVerificationType1Type0",
        "UnbanUserResponse200PasskeysItemVerificationType2Type0",
    ]
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.unban_user_response_200_passkeys_item_verification_type_0 import (
            UnbanUserResponse200PasskeysItemVerificationType0,
        )
        from ..models.unban_user_response_200_passkeys_item_verification_type_1_type_0 import (
            UnbanUserResponse200PasskeysItemVerificationType1Type0,
        )

        object_ = self.object_.value

        name = self.name

        last_used_at = self.last_used_at

        verification: Dict[str, Any]
        if isinstance(self.verification, UnbanUserResponse200PasskeysItemVerificationType0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, UnbanUserResponse200PasskeysItemVerificationType1Type0):
            verification = self.verification.to_dict()
        else:
            verification = self.verification.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "name": name,
                "last_used_at": last_used_at,
                "verification": verification,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.unban_user_response_200_passkeys_item_verification_type_0 import (
            UnbanUserResponse200PasskeysItemVerificationType0,
        )
        from ..models.unban_user_response_200_passkeys_item_verification_type_1_type_0 import (
            UnbanUserResponse200PasskeysItemVerificationType1Type0,
        )
        from ..models.unban_user_response_200_passkeys_item_verification_type_2_type_0 import (
            UnbanUserResponse200PasskeysItemVerificationType2Type0,
        )

        d = src_dict.copy()
        object_ = UnbanUserResponse200PasskeysItemObject(d.pop("object"))

        name = d.pop("name")

        last_used_at = d.pop("last_used_at")

        def _parse_verification(
            data: object,
        ) -> Union[
            "UnbanUserResponse200PasskeysItemVerificationType0",
            "UnbanUserResponse200PasskeysItemVerificationType1Type0",
            "UnbanUserResponse200PasskeysItemVerificationType2Type0",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_0 = UnbanUserResponse200PasskeysItemVerificationType0.from_dict(data)

                return verification_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_1_type_0 = UnbanUserResponse200PasskeysItemVerificationType1Type0.from_dict(data)

                return verification_type_1_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            verification_type_2_type_0 = UnbanUserResponse200PasskeysItemVerificationType2Type0.from_dict(data)

            return verification_type_2_type_0

        verification = _parse_verification(d.pop("verification"))

        id = d.pop("id", UNSET)

        unban_user_response_200_passkeys_item = cls(
            object_=object_,
            name=name,
            last_used_at=last_used_at,
            verification=verification,
            id=id,
        )

        return unban_user_response_200_passkeys_item
