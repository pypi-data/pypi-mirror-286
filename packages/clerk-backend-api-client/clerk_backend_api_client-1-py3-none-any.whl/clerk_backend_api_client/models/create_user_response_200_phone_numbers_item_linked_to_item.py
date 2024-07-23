from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.create_user_response_200_phone_numbers_item_linked_to_item_type import (
    CreateUserResponse200PhoneNumbersItemLinkedToItemType,
)

T = TypeVar("T", bound="CreateUserResponse200PhoneNumbersItemLinkedToItem")


@_attrs_define
class CreateUserResponse200PhoneNumbersItemLinkedToItem:
    """
    Attributes:
        type (CreateUserResponse200PhoneNumbersItemLinkedToItemType):
        id (str):
    """

    type: CreateUserResponse200PhoneNumbersItemLinkedToItemType
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
        type = CreateUserResponse200PhoneNumbersItemLinkedToItemType(d.pop("type"))

        id = d.pop("id")

        create_user_response_200_phone_numbers_item_linked_to_item = cls(
            type=type,
            id=id,
        )

        return create_user_response_200_phone_numbers_item_linked_to_item
