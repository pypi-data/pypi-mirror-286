from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.user_email_addresses_item_linked_to_item_type import UserEmailAddressesItemLinkedToItemType

T = TypeVar("T", bound="UserEmailAddressesItemLinkedToItem")


@_attrs_define
class UserEmailAddressesItemLinkedToItem:
    """
    Attributes:
        type (UserEmailAddressesItemLinkedToItemType):
        id (str):
    """

    type: UserEmailAddressesItemLinkedToItemType
    id: str

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = UserEmailAddressesItemLinkedToItemType(d.pop("type"))

        id = d.pop("id")

        user_email_addresses_item_linked_to_item = cls(
            type=type,
            id=id,
        )

        return user_email_addresses_item_linked_to_item
