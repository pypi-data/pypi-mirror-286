from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.update_user_metadata_response_200_email_addresses_item_linked_to_item_type import (
    UpdateUserMetadataResponse200EmailAddressesItemLinkedToItemType,
)

T = TypeVar("T", bound="UpdateUserMetadataResponse200EmailAddressesItemLinkedToItem")


@_attrs_define
class UpdateUserMetadataResponse200EmailAddressesItemLinkedToItem:
    """
    Attributes:
        type (UpdateUserMetadataResponse200EmailAddressesItemLinkedToItemType):
        id (str):
    """

    type: UpdateUserMetadataResponse200EmailAddressesItemLinkedToItemType
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
        type = UpdateUserMetadataResponse200EmailAddressesItemLinkedToItemType(d.pop("type"))

        id = d.pop("id")

        update_user_metadata_response_200_email_addresses_item_linked_to_item = cls(
            type=type,
            id=id,
        )

        return update_user_metadata_response_200_email_addresses_item_linked_to_item
