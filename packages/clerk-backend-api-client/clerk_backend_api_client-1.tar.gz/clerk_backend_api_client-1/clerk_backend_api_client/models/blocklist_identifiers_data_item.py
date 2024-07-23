from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..models.blocklist_identifiers_data_item_identifier_type import BlocklistIdentifiersDataItemIdentifierType
from ..models.blocklist_identifiers_data_item_object import BlocklistIdentifiersDataItemObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="BlocklistIdentifiersDataItem")


@_attrs_define
class BlocklistIdentifiersDataItem:
    """
    Attributes:
        object_ (Union[Unset, BlocklistIdentifiersDataItemObject]): String representing the object's type. Objects of
            the same type share the same value.
        id (Union[Unset, str]):
        identifier (Union[Unset, str]): An email address, email domain, phone number or web3 wallet.
        identifier_type (Union[Unset, BlocklistIdentifiersDataItemIdentifierType]):
        instance_id (Union[Unset, str]):
        created_at (Union[Unset, int]): Unix timestamp of creation
        updated_at (Union[Unset, int]): Unix timestamp of last update.
    """

    object_: Union[Unset, BlocklistIdentifiersDataItemObject] = UNSET
    id: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    identifier_type: Union[Unset, BlocklistIdentifiersDataItemIdentifierType] = UNSET
    instance_id: Union[Unset, str] = UNSET
    created_at: Union[Unset, int] = UNSET
    updated_at: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_: Union[Unset, str] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.value

        id = self.id

        identifier = self.identifier

        identifier_type: Union[Unset, str] = UNSET
        if not isinstance(self.identifier_type, Unset):
            identifier_type = self.identifier_type.value

        instance_id = self.instance_id

        created_at = self.created_at

        updated_at = self.updated_at

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if object_ is not UNSET:
            field_dict["object"] = object_
        if id is not UNSET:
            field_dict["id"] = id
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if identifier_type is not UNSET:
            field_dict["identifier_type"] = identifier_type
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _object_ = d.pop("object", UNSET)
        object_: Union[Unset, BlocklistIdentifiersDataItemObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = BlocklistIdentifiersDataItemObject(_object_)

        id = d.pop("id", UNSET)

        identifier = d.pop("identifier", UNSET)

        _identifier_type = d.pop("identifier_type", UNSET)
        identifier_type: Union[Unset, BlocklistIdentifiersDataItemIdentifierType]
        if isinstance(_identifier_type, Unset):
            identifier_type = UNSET
        else:
            identifier_type = BlocklistIdentifiersDataItemIdentifierType(_identifier_type)

        instance_id = d.pop("instance_id", UNSET)

        created_at = d.pop("created_at", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        blocklist_identifiers_data_item = cls(
            object_=object_,
            id=id,
            identifier=identifier,
            identifier_type=identifier_type,
            instance_id=instance_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        return blocklist_identifiers_data_item
