from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.update_phone_number_response_200_linked_to_item_type import UpdatePhoneNumberResponse200LinkedToItemType

T = TypeVar("T", bound="UpdatePhoneNumberResponse200LinkedToItem")


@_attrs_define
class UpdatePhoneNumberResponse200LinkedToItem:
    """
    Attributes:
        type (UpdatePhoneNumberResponse200LinkedToItemType):
        id (str):
    """

    type: UpdatePhoneNumberResponse200LinkedToItemType
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
        type = UpdatePhoneNumberResponse200LinkedToItemType(d.pop("type"))

        id = d.pop("id")

        update_phone_number_response_200_linked_to_item = cls(
            type=type,
            id=id,
        )

        return update_phone_number_response_200_linked_to_item
