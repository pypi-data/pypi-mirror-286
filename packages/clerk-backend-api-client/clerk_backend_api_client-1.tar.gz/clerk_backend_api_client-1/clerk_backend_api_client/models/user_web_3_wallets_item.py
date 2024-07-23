from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..models.user_web_3_wallets_item_object import UserWeb3WalletsItemObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_web_3_wallets_item_verification_type_0 import UserWeb3WalletsItemVerificationType0
    from ..models.user_web_3_wallets_item_verification_type_1 import UserWeb3WalletsItemVerificationType1
    from ..models.user_web_3_wallets_item_verification_type_2_type_0 import UserWeb3WalletsItemVerificationType2Type0
    from ..models.user_web_3_wallets_item_verification_type_2_type_1 import UserWeb3WalletsItemVerificationType2Type1
    from ..models.user_web_3_wallets_item_verification_type_3_type_0 import UserWeb3WalletsItemVerificationType3Type0
    from ..models.user_web_3_wallets_item_verification_type_3_type_1 import UserWeb3WalletsItemVerificationType3Type1


T = TypeVar("T", bound="UserWeb3WalletsItem")


@_attrs_define
class UserWeb3WalletsItem:
    """
    Attributes:
        object_ (UserWeb3WalletsItemObject): String representing the object's type. Objects of the same type share the
            same value.
        web3_wallet (str):
        verification (Union['UserWeb3WalletsItemVerificationType0', 'UserWeb3WalletsItemVerificationType1',
            'UserWeb3WalletsItemVerificationType2Type0', 'UserWeb3WalletsItemVerificationType2Type1',
            'UserWeb3WalletsItemVerificationType3Type0', 'UserWeb3WalletsItemVerificationType3Type1']):
        created_at (int): Unix timestamp of creation
        updated_at (int): Unix timestamp of creation
        id (Union[Unset, str]):
    """

    object_: UserWeb3WalletsItemObject
    web3_wallet: str
    verification: Union[
        "UserWeb3WalletsItemVerificationType0",
        "UserWeb3WalletsItemVerificationType1",
        "UserWeb3WalletsItemVerificationType2Type0",
        "UserWeb3WalletsItemVerificationType2Type1",
        "UserWeb3WalletsItemVerificationType3Type0",
        "UserWeb3WalletsItemVerificationType3Type1",
    ]
    created_at: int
    updated_at: int
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.user_web_3_wallets_item_verification_type_0 import UserWeb3WalletsItemVerificationType0
        from ..models.user_web_3_wallets_item_verification_type_1 import UserWeb3WalletsItemVerificationType1
        from ..models.user_web_3_wallets_item_verification_type_2_type_0 import (
            UserWeb3WalletsItemVerificationType2Type0,
        )
        from ..models.user_web_3_wallets_item_verification_type_2_type_1 import (
            UserWeb3WalletsItemVerificationType2Type1,
        )
        from ..models.user_web_3_wallets_item_verification_type_3_type_0 import (
            UserWeb3WalletsItemVerificationType3Type0,
        )

        object_ = self.object_.value

        web3_wallet = self.web3_wallet

        verification: Dict[str, Any]
        if isinstance(self.verification, UserWeb3WalletsItemVerificationType0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, UserWeb3WalletsItemVerificationType1):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, UserWeb3WalletsItemVerificationType2Type0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, UserWeb3WalletsItemVerificationType2Type1):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, UserWeb3WalletsItemVerificationType3Type0):
            verification = self.verification.to_dict()
        else:
            verification = self.verification.to_dict()

        created_at = self.created_at

        updated_at = self.updated_at

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "web3_wallet": web3_wallet,
                "verification": verification,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_web_3_wallets_item_verification_type_0 import UserWeb3WalletsItemVerificationType0
        from ..models.user_web_3_wallets_item_verification_type_1 import UserWeb3WalletsItemVerificationType1
        from ..models.user_web_3_wallets_item_verification_type_2_type_0 import (
            UserWeb3WalletsItemVerificationType2Type0,
        )
        from ..models.user_web_3_wallets_item_verification_type_2_type_1 import (
            UserWeb3WalletsItemVerificationType2Type1,
        )
        from ..models.user_web_3_wallets_item_verification_type_3_type_0 import (
            UserWeb3WalletsItemVerificationType3Type0,
        )
        from ..models.user_web_3_wallets_item_verification_type_3_type_1 import (
            UserWeb3WalletsItemVerificationType3Type1,
        )

        d = src_dict.copy()
        object_ = UserWeb3WalletsItemObject(d.pop("object"))

        web3_wallet = d.pop("web3_wallet")

        def _parse_verification(
            data: object,
        ) -> Union[
            "UserWeb3WalletsItemVerificationType0",
            "UserWeb3WalletsItemVerificationType1",
            "UserWeb3WalletsItemVerificationType2Type0",
            "UserWeb3WalletsItemVerificationType2Type1",
            "UserWeb3WalletsItemVerificationType3Type0",
            "UserWeb3WalletsItemVerificationType3Type1",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_0 = UserWeb3WalletsItemVerificationType0.from_dict(data)

                return verification_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_1 = UserWeb3WalletsItemVerificationType1.from_dict(data)

                return verification_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_2_type_0 = UserWeb3WalletsItemVerificationType2Type0.from_dict(data)

                return verification_type_2_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_2_type_1 = UserWeb3WalletsItemVerificationType2Type1.from_dict(data)

                return verification_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_3_type_0 = UserWeb3WalletsItemVerificationType3Type0.from_dict(data)

                return verification_type_3_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            verification_type_3_type_1 = UserWeb3WalletsItemVerificationType3Type1.from_dict(data)

            return verification_type_3_type_1

        verification = _parse_verification(d.pop("verification"))

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        id = d.pop("id", UNSET)

        user_web_3_wallets_item = cls(
            object_=object_,
            web3_wallet=web3_wallet,
            verification=verification,
            created_at=created_at,
            updated_at=updated_at,
            id=id,
        )

        return user_web_3_wallets_item
