from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.get_user_list_response_200_item_email_addresses_item_linked_to_item_type import (
    GetUserListResponse200ItemEmailAddressesItemLinkedToItemType,
)

T = TypeVar("T", bound="GetUserListResponse200ItemEmailAddressesItemLinkedToItem")


@_attrs_define
class GetUserListResponse200ItemEmailAddressesItemLinkedToItem:
    """
    Attributes:
        type (GetUserListResponse200ItemEmailAddressesItemLinkedToItemType):
        id (str):
    """

    type: GetUserListResponse200ItemEmailAddressesItemLinkedToItemType
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
        type = GetUserListResponse200ItemEmailAddressesItemLinkedToItemType(d.pop("type"))

        id = d.pop("id")

        get_user_list_response_200_item_email_addresses_item_linked_to_item = cls(
            type=type,
            id=id,
        )

        return get_user_list_response_200_item_email_addresses_item_linked_to_item
