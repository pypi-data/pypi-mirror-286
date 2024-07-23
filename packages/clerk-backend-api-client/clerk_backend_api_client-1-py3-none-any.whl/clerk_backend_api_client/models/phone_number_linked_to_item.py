from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.phone_number_linked_to_item_type import PhoneNumberLinkedToItemType

T = TypeVar("T", bound="PhoneNumberLinkedToItem")


@_attrs_define
class PhoneNumberLinkedToItem:
    """
    Attributes:
        type (PhoneNumberLinkedToItemType):
        id (str):
    """

    type: PhoneNumberLinkedToItemType
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
        type = PhoneNumberLinkedToItemType(d.pop("type"))

        id = d.pop("id")

        phone_number_linked_to_item = cls(
            type=type,
            id=id,
        )

        return phone_number_linked_to_item
