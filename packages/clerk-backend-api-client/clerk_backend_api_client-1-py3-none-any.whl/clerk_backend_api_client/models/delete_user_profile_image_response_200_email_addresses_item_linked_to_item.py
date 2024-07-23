from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.delete_user_profile_image_response_200_email_addresses_item_linked_to_item_type import (
    DeleteUserProfileImageResponse200EmailAddressesItemLinkedToItemType,
)

T = TypeVar("T", bound="DeleteUserProfileImageResponse200EmailAddressesItemLinkedToItem")


@_attrs_define
class DeleteUserProfileImageResponse200EmailAddressesItemLinkedToItem:
    """
    Attributes:
        type (DeleteUserProfileImageResponse200EmailAddressesItemLinkedToItemType):
        id (str):
    """

    type: DeleteUserProfileImageResponse200EmailAddressesItemLinkedToItemType
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
        type = DeleteUserProfileImageResponse200EmailAddressesItemLinkedToItemType(d.pop("type"))

        id = d.pop("id")

        delete_user_profile_image_response_200_email_addresses_item_linked_to_item = cls(
            type=type,
            id=id,
        )

        return delete_user_profile_image_response_200_email_addresses_item_linked_to_item
