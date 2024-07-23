from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..models.list_allowlist_identifiers_response_200_item_identifier_type import (
    ListAllowlistIdentifiersResponse200ItemIdentifierType,
)
from ..models.list_allowlist_identifiers_response_200_item_object import ListAllowlistIdentifiersResponse200ItemObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAllowlistIdentifiersResponse200Item")


@_attrs_define
class ListAllowlistIdentifiersResponse200Item:
    """
    Attributes:
        object_ (Union[Unset, ListAllowlistIdentifiersResponse200ItemObject]): String representing the object's type.
            Objects of the same type share the same value.
        id (Union[Unset, str]):
        invitation_id (Union[Unset, str]):
        identifier (Union[Unset, str]): An email address or a phone number.
        identifier_type (Union[Unset, ListAllowlistIdentifiersResponse200ItemIdentifierType]):
        instance_id (Union[Unset, str]):
        created_at (Union[Unset, int]): Unix timestamp of creation
        updated_at (Union[Unset, int]): Unix timestamp of last update.
    """

    object_: Union[Unset, ListAllowlistIdentifiersResponse200ItemObject] = UNSET
    id: Union[Unset, str] = UNSET
    invitation_id: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    identifier_type: Union[Unset, ListAllowlistIdentifiersResponse200ItemIdentifierType] = UNSET
    instance_id: Union[Unset, str] = UNSET
    created_at: Union[Unset, int] = UNSET
    updated_at: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_: Union[Unset, str] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.value

        id = self.id

        invitation_id = self.invitation_id

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
        if invitation_id is not UNSET:
            field_dict["invitation_id"] = invitation_id
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
        object_: Union[Unset, ListAllowlistIdentifiersResponse200ItemObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = ListAllowlistIdentifiersResponse200ItemObject(_object_)

        id = d.pop("id", UNSET)

        invitation_id = d.pop("invitation_id", UNSET)

        identifier = d.pop("identifier", UNSET)

        _identifier_type = d.pop("identifier_type", UNSET)
        identifier_type: Union[Unset, ListAllowlistIdentifiersResponse200ItemIdentifierType]
        if isinstance(_identifier_type, Unset):
            identifier_type = UNSET
        else:
            identifier_type = ListAllowlistIdentifiersResponse200ItemIdentifierType(_identifier_type)

        instance_id = d.pop("instance_id", UNSET)

        created_at = d.pop("created_at", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        list_allowlist_identifiers_response_200_item = cls(
            object_=object_,
            id=id,
            invitation_id=invitation_id,
            identifier=identifier,
            identifier_type=identifier_type,
            instance_id=instance_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        return list_allowlist_identifiers_response_200_item
