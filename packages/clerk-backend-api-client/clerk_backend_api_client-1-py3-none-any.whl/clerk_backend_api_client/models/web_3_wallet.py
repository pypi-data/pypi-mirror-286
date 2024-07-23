from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..models.web_3_wallet_object import Web3WalletObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.web_3_wallet_verification_type_0 import Web3WalletVerificationType0
    from ..models.web_3_wallet_verification_type_1 import Web3WalletVerificationType1
    from ..models.web_3_wallet_verification_type_2_type_0 import Web3WalletVerificationType2Type0
    from ..models.web_3_wallet_verification_type_2_type_1 import Web3WalletVerificationType2Type1
    from ..models.web_3_wallet_verification_type_3_type_0 import Web3WalletVerificationType3Type0
    from ..models.web_3_wallet_verification_type_3_type_1 import Web3WalletVerificationType3Type1


T = TypeVar("T", bound="Web3Wallet")


@_attrs_define
class Web3Wallet:
    """
    Attributes:
        object_ (Web3WalletObject): String representing the object's type. Objects of the same type share the same
            value.
        web3_wallet (str):
        verification (Union['Web3WalletVerificationType0', 'Web3WalletVerificationType1',
            'Web3WalletVerificationType2Type0', 'Web3WalletVerificationType2Type1', 'Web3WalletVerificationType3Type0',
            'Web3WalletVerificationType3Type1']):
        created_at (int): Unix timestamp of creation
        updated_at (int): Unix timestamp of creation
        id (Union[Unset, str]):
    """

    object_: Web3WalletObject
    web3_wallet: str
    verification: Union[
        "Web3WalletVerificationType0",
        "Web3WalletVerificationType1",
        "Web3WalletVerificationType2Type0",
        "Web3WalletVerificationType2Type1",
        "Web3WalletVerificationType3Type0",
        "Web3WalletVerificationType3Type1",
    ]
    created_at: int
    updated_at: int
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.web_3_wallet_verification_type_0 import Web3WalletVerificationType0
        from ..models.web_3_wallet_verification_type_1 import Web3WalletVerificationType1
        from ..models.web_3_wallet_verification_type_2_type_0 import Web3WalletVerificationType2Type0
        from ..models.web_3_wallet_verification_type_2_type_1 import Web3WalletVerificationType2Type1
        from ..models.web_3_wallet_verification_type_3_type_0 import Web3WalletVerificationType3Type0

        object_ = self.object_.value

        web3_wallet = self.web3_wallet

        verification: Dict[str, Any]
        if isinstance(self.verification, Web3WalletVerificationType0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, Web3WalletVerificationType1):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, Web3WalletVerificationType2Type0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, Web3WalletVerificationType2Type1):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, Web3WalletVerificationType3Type0):
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
        from ..models.web_3_wallet_verification_type_0 import Web3WalletVerificationType0
        from ..models.web_3_wallet_verification_type_1 import Web3WalletVerificationType1
        from ..models.web_3_wallet_verification_type_2_type_0 import Web3WalletVerificationType2Type0
        from ..models.web_3_wallet_verification_type_2_type_1 import Web3WalletVerificationType2Type1
        from ..models.web_3_wallet_verification_type_3_type_0 import Web3WalletVerificationType3Type0
        from ..models.web_3_wallet_verification_type_3_type_1 import Web3WalletVerificationType3Type1

        d = src_dict.copy()
        object_ = Web3WalletObject(d.pop("object"))

        web3_wallet = d.pop("web3_wallet")

        def _parse_verification(
            data: object,
        ) -> Union[
            "Web3WalletVerificationType0",
            "Web3WalletVerificationType1",
            "Web3WalletVerificationType2Type0",
            "Web3WalletVerificationType2Type1",
            "Web3WalletVerificationType3Type0",
            "Web3WalletVerificationType3Type1",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_0 = Web3WalletVerificationType0.from_dict(data)

                return verification_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_1 = Web3WalletVerificationType1.from_dict(data)

                return verification_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_2_type_0 = Web3WalletVerificationType2Type0.from_dict(data)

                return verification_type_2_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_2_type_1 = Web3WalletVerificationType2Type1.from_dict(data)

                return verification_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_3_type_0 = Web3WalletVerificationType3Type0.from_dict(data)

                return verification_type_3_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            verification_type_3_type_1 = Web3WalletVerificationType3Type1.from_dict(data)

            return verification_type_3_type_1

        verification = _parse_verification(d.pop("verification"))

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        id = d.pop("id", UNSET)

        web_3_wallet = cls(
            object_=object_,
            web3_wallet=web3_wallet,
            verification=verification,
            created_at=created_at,
            updated_at=updated_at,
            id=id,
        )

        return web_3_wallet
