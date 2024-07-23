from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.email_address_linked_to_item_type import EmailAddressLinkedToItemType

T = TypeVar("T", bound="EmailAddressLinkedToItem")


@_attrs_define
class EmailAddressLinkedToItem:
    """
    Attributes:
        type (EmailAddressLinkedToItemType):
        id (str):
    """

    type: EmailAddressLinkedToItemType
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
        type = EmailAddressLinkedToItemType(d.pop("type"))

        id = d.pop("id")

        email_address_linked_to_item = cls(
            type=type,
            id=id,
        )

        return email_address_linked_to_item
