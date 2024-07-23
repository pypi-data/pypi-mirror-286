from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.get_user_list_response_200_item_phone_numbers_item_linked_to_item_type import (
    GetUserListResponse200ItemPhoneNumbersItemLinkedToItemType,
)

T = TypeVar("T", bound="GetUserListResponse200ItemPhoneNumbersItemLinkedToItem")


@_attrs_define
class GetUserListResponse200ItemPhoneNumbersItemLinkedToItem:
    """
    Attributes:
        type (GetUserListResponse200ItemPhoneNumbersItemLinkedToItemType):
        id (str):
    """

    type: GetUserListResponse200ItemPhoneNumbersItemLinkedToItemType
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
        type = GetUserListResponse200ItemPhoneNumbersItemLinkedToItemType(d.pop("type"))

        id = d.pop("id")

        get_user_list_response_200_item_phone_numbers_item_linked_to_item = cls(
            type=type,
            id=id,
        )

        return get_user_list_response_200_item_phone_numbers_item_linked_to_item
