from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.update_email_address_response_200_linked_to_item_type import UpdateEmailAddressResponse200LinkedToItemType

T = TypeVar("T", bound="UpdateEmailAddressResponse200LinkedToItem")


@_attrs_define
class UpdateEmailAddressResponse200LinkedToItem:
    """
    Attributes:
        type (UpdateEmailAddressResponse200LinkedToItemType):
        id (str):
    """

    type: UpdateEmailAddressResponse200LinkedToItemType
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
        type = UpdateEmailAddressResponse200LinkedToItemType(d.pop("type"))

        id = d.pop("id")

        update_email_address_response_200_linked_to_item = cls(
            type=type,
            id=id,
        )

        return update_email_address_response_200_linked_to_item
