from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.get_email_address_response_200_linked_to_item_type import GetEmailAddressResponse200LinkedToItemType

T = TypeVar("T", bound="GetEmailAddressResponse200LinkedToItem")


@_attrs_define
class GetEmailAddressResponse200LinkedToItem:
    """
    Attributes:
        type (GetEmailAddressResponse200LinkedToItemType):
        id (str):
    """

    type: GetEmailAddressResponse200LinkedToItemType
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
        type = GetEmailAddressResponse200LinkedToItemType(d.pop("type"))

        id = d.pop("id")

        get_email_address_response_200_linked_to_item = cls(
            type=type,
            id=id,
        )

        return get_email_address_response_200_linked_to_item
