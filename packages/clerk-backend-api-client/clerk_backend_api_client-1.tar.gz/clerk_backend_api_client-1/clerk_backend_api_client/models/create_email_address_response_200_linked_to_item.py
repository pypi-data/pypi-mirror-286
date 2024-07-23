from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.create_email_address_response_200_linked_to_item_type import CreateEmailAddressResponse200LinkedToItemType

T = TypeVar("T", bound="CreateEmailAddressResponse200LinkedToItem")


@_attrs_define
class CreateEmailAddressResponse200LinkedToItem:
    """
    Attributes:
        type (CreateEmailAddressResponse200LinkedToItemType):
        id (str):
    """

    type: CreateEmailAddressResponse200LinkedToItemType
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
        type = CreateEmailAddressResponse200LinkedToItemType(d.pop("type"))

        id = d.pop("id")

        create_email_address_response_200_linked_to_item = cls(
            type=type,
            id=id,
        )

        return create_email_address_response_200_linked_to_item
