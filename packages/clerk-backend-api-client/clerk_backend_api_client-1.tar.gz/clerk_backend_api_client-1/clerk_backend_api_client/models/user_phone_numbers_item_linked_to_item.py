from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.user_phone_numbers_item_linked_to_item_type import UserPhoneNumbersItemLinkedToItemType

T = TypeVar("T", bound="UserPhoneNumbersItemLinkedToItem")


@_attrs_define
class UserPhoneNumbersItemLinkedToItem:
    """
    Attributes:
        type (UserPhoneNumbersItemLinkedToItemType):
        id (str):
    """

    type: UserPhoneNumbersItemLinkedToItemType
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
        type = UserPhoneNumbersItemLinkedToItemType(d.pop("type"))

        id = d.pop("id")

        user_phone_numbers_item_linked_to_item = cls(
            type=type,
            id=id,
        )

        return user_phone_numbers_item_linked_to_item
