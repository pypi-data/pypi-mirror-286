from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.set_user_profile_image_response_200_phone_numbers_item_linked_to_item_type import (
    SetUserProfileImageResponse200PhoneNumbersItemLinkedToItemType,
)

T = TypeVar("T", bound="SetUserProfileImageResponse200PhoneNumbersItemLinkedToItem")


@_attrs_define
class SetUserProfileImageResponse200PhoneNumbersItemLinkedToItem:
    """
    Attributes:
        type (SetUserProfileImageResponse200PhoneNumbersItemLinkedToItemType):
        id (str):
    """

    type: SetUserProfileImageResponse200PhoneNumbersItemLinkedToItemType
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
        type = SetUserProfileImageResponse200PhoneNumbersItemLinkedToItemType(d.pop("type"))

        id = d.pop("id")

        set_user_profile_image_response_200_phone_numbers_item_linked_to_item = cls(
            type=type,
            id=id,
        )

        return set_user_profile_image_response_200_phone_numbers_item_linked_to_item
