from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..models.get_user_list_response_200_item_email_addresses_item_object import (
    GetUserListResponse200ItemEmailAddressesItemObject,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_user_list_response_200_item_email_addresses_item_linked_to_item import (
        GetUserListResponse200ItemEmailAddressesItemLinkedToItem,
    )
    from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_0 import (
        GetUserListResponse200ItemEmailAddressesItemVerificationType0,
    )
    from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_1 import (
        GetUserListResponse200ItemEmailAddressesItemVerificationType1,
    )
    from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_2 import (
        GetUserListResponse200ItemEmailAddressesItemVerificationType2,
    )
    from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_3_type_0 import (
        GetUserListResponse200ItemEmailAddressesItemVerificationType3Type0,
    )
    from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_3_type_1 import (
        GetUserListResponse200ItemEmailAddressesItemVerificationType3Type1,
    )
    from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_3_type_2 import (
        GetUserListResponse200ItemEmailAddressesItemVerificationType3Type2,
    )
    from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_4_type_0 import (
        GetUserListResponse200ItemEmailAddressesItemVerificationType4Type0,
    )
    from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_4_type_1 import (
        GetUserListResponse200ItemEmailAddressesItemVerificationType4Type1,
    )
    from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_4_type_2 import (
        GetUserListResponse200ItemEmailAddressesItemVerificationType4Type2,
    )


T = TypeVar("T", bound="GetUserListResponse200ItemEmailAddressesItem")


@_attrs_define
class GetUserListResponse200ItemEmailAddressesItem:
    """
    Attributes:
        object_ (GetUserListResponse200ItemEmailAddressesItemObject): String representing the object's type. Objects of
            the same type share the same value.
        email_address (str):
        reserved (bool):
        verification (Union['GetUserListResponse200ItemEmailAddressesItemVerificationType0',
            'GetUserListResponse200ItemEmailAddressesItemVerificationType1',
            'GetUserListResponse200ItemEmailAddressesItemVerificationType2',
            'GetUserListResponse200ItemEmailAddressesItemVerificationType3Type0',
            'GetUserListResponse200ItemEmailAddressesItemVerificationType3Type1',
            'GetUserListResponse200ItemEmailAddressesItemVerificationType3Type2',
            'GetUserListResponse200ItemEmailAddressesItemVerificationType4Type0',
            'GetUserListResponse200ItemEmailAddressesItemVerificationType4Type1',
            'GetUserListResponse200ItemEmailAddressesItemVerificationType4Type2']):
        linked_to (List['GetUserListResponse200ItemEmailAddressesItemLinkedToItem']):
        created_at (int): Unix timestamp of creation
        updated_at (int): Unix timestamp of creation
        id (Union[Unset, str]):
    """

    object_: GetUserListResponse200ItemEmailAddressesItemObject
    email_address: str
    reserved: bool
    verification: Union[
        "GetUserListResponse200ItemEmailAddressesItemVerificationType0",
        "GetUserListResponse200ItemEmailAddressesItemVerificationType1",
        "GetUserListResponse200ItemEmailAddressesItemVerificationType2",
        "GetUserListResponse200ItemEmailAddressesItemVerificationType3Type0",
        "GetUserListResponse200ItemEmailAddressesItemVerificationType3Type1",
        "GetUserListResponse200ItemEmailAddressesItemVerificationType3Type2",
        "GetUserListResponse200ItemEmailAddressesItemVerificationType4Type0",
        "GetUserListResponse200ItemEmailAddressesItemVerificationType4Type1",
        "GetUserListResponse200ItemEmailAddressesItemVerificationType4Type2",
    ]
    linked_to: List["GetUserListResponse200ItemEmailAddressesItemLinkedToItem"]
    created_at: int
    updated_at: int
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_0 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType0,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_1 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType1,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_2 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType2,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_3_type_0 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType3Type0,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_3_type_1 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType3Type1,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_3_type_2 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType3Type2,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_4_type_0 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType4Type0,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_4_type_1 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType4Type1,
        )

        object_ = self.object_.value

        email_address = self.email_address

        reserved = self.reserved

        verification: Dict[str, Any]
        if isinstance(self.verification, GetUserListResponse200ItemEmailAddressesItemVerificationType0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, GetUserListResponse200ItemEmailAddressesItemVerificationType1):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, GetUserListResponse200ItemEmailAddressesItemVerificationType2):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, GetUserListResponse200ItemEmailAddressesItemVerificationType3Type0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, GetUserListResponse200ItemEmailAddressesItemVerificationType3Type1):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, GetUserListResponse200ItemEmailAddressesItemVerificationType3Type2):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, GetUserListResponse200ItemEmailAddressesItemVerificationType4Type0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, GetUserListResponse200ItemEmailAddressesItemVerificationType4Type1):
            verification = self.verification.to_dict()
        else:
            verification = self.verification.to_dict()

        linked_to = []
        for linked_to_item_data in self.linked_to:
            linked_to_item = linked_to_item_data.to_dict()
            linked_to.append(linked_to_item)

        created_at = self.created_at

        updated_at = self.updated_at

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "email_address": email_address,
                "reserved": reserved,
                "verification": verification,
                "linked_to": linked_to,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_user_list_response_200_item_email_addresses_item_linked_to_item import (
            GetUserListResponse200ItemEmailAddressesItemLinkedToItem,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_0 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType0,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_1 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType1,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_2 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType2,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_3_type_0 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType3Type0,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_3_type_1 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType3Type1,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_3_type_2 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType3Type2,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_4_type_0 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType4Type0,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_4_type_1 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType4Type1,
        )
        from ..models.get_user_list_response_200_item_email_addresses_item_verification_type_4_type_2 import (
            GetUserListResponse200ItemEmailAddressesItemVerificationType4Type2,
        )

        d = src_dict.copy()
        object_ = GetUserListResponse200ItemEmailAddressesItemObject(d.pop("object"))

        email_address = d.pop("email_address")

        reserved = d.pop("reserved")

        def _parse_verification(
            data: object,
        ) -> Union[
            "GetUserListResponse200ItemEmailAddressesItemVerificationType0",
            "GetUserListResponse200ItemEmailAddressesItemVerificationType1",
            "GetUserListResponse200ItemEmailAddressesItemVerificationType2",
            "GetUserListResponse200ItemEmailAddressesItemVerificationType3Type0",
            "GetUserListResponse200ItemEmailAddressesItemVerificationType3Type1",
            "GetUserListResponse200ItemEmailAddressesItemVerificationType3Type2",
            "GetUserListResponse200ItemEmailAddressesItemVerificationType4Type0",
            "GetUserListResponse200ItemEmailAddressesItemVerificationType4Type1",
            "GetUserListResponse200ItemEmailAddressesItemVerificationType4Type2",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_0 = GetUserListResponse200ItemEmailAddressesItemVerificationType0.from_dict(data)

                return verification_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_1 = GetUserListResponse200ItemEmailAddressesItemVerificationType1.from_dict(data)

                return verification_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_2 = GetUserListResponse200ItemEmailAddressesItemVerificationType2.from_dict(data)

                return verification_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_3_type_0 = (
                    GetUserListResponse200ItemEmailAddressesItemVerificationType3Type0.from_dict(data)
                )

                return verification_type_3_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_3_type_1 = (
                    GetUserListResponse200ItemEmailAddressesItemVerificationType3Type1.from_dict(data)
                )

                return verification_type_3_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_3_type_2 = (
                    GetUserListResponse200ItemEmailAddressesItemVerificationType3Type2.from_dict(data)
                )

                return verification_type_3_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_4_type_0 = (
                    GetUserListResponse200ItemEmailAddressesItemVerificationType4Type0.from_dict(data)
                )

                return verification_type_4_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_4_type_1 = (
                    GetUserListResponse200ItemEmailAddressesItemVerificationType4Type1.from_dict(data)
                )

                return verification_type_4_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            verification_type_4_type_2 = GetUserListResponse200ItemEmailAddressesItemVerificationType4Type2.from_dict(
                data
            )

            return verification_type_4_type_2

        verification = _parse_verification(d.pop("verification"))

        linked_to = []
        _linked_to = d.pop("linked_to")
        for linked_to_item_data in _linked_to:
            linked_to_item = GetUserListResponse200ItemEmailAddressesItemLinkedToItem.from_dict(linked_to_item_data)

            linked_to.append(linked_to_item)

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        id = d.pop("id", UNSET)

        get_user_list_response_200_item_email_addresses_item = cls(
            object_=object_,
            email_address=email_address,
            reserved=reserved,
            verification=verification,
            linked_to=linked_to,
            created_at=created_at,
            updated_at=updated_at,
            id=id,
        )

        return get_user_list_response_200_item_email_addresses_item
