from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_instance_auth_config_response_200_object import UpdateInstanceAuthConfigResponse200Object
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateInstanceAuthConfigResponse200")


@_attrs_define
class UpdateInstanceAuthConfigResponse200:
    """
    Attributes:
        object_ (Union[Unset, UpdateInstanceAuthConfigResponse200Object]): String representing the object's type.
            Objects of the same type share the same value.
        id (Union[Unset, str]):
        restricted_to_allowlist (Union[Unset, bool]):
        from_email_address (Union[Unset, str]):
        progressive_sign_up (Union[Unset, bool]):
        enhanced_email_deliverability (Union[Unset, bool]):
    """

    object_: Union[Unset, UpdateInstanceAuthConfigResponse200Object] = UNSET
    id: Union[Unset, str] = UNSET
    restricted_to_allowlist: Union[Unset, bool] = UNSET
    from_email_address: Union[Unset, str] = UNSET
    progressive_sign_up: Union[Unset, bool] = UNSET
    enhanced_email_deliverability: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_: Union[Unset, str] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.value

        id = self.id

        restricted_to_allowlist = self.restricted_to_allowlist

        from_email_address = self.from_email_address

        progressive_sign_up = self.progressive_sign_up

        enhanced_email_deliverability = self.enhanced_email_deliverability

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_ is not UNSET:
            field_dict["object"] = object_
        if id is not UNSET:
            field_dict["id"] = id
        if restricted_to_allowlist is not UNSET:
            field_dict["restricted_to_allowlist"] = restricted_to_allowlist
        if from_email_address is not UNSET:
            field_dict["from_email_address"] = from_email_address
        if progressive_sign_up is not UNSET:
            field_dict["progressive_sign_up"] = progressive_sign_up
        if enhanced_email_deliverability is not UNSET:
            field_dict["enhanced_email_deliverability"] = enhanced_email_deliverability

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _object_ = d.pop("object", UNSET)
        object_: Union[Unset, UpdateInstanceAuthConfigResponse200Object]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = UpdateInstanceAuthConfigResponse200Object(_object_)

        id = d.pop("id", UNSET)

        restricted_to_allowlist = d.pop("restricted_to_allowlist", UNSET)

        from_email_address = d.pop("from_email_address", UNSET)

        progressive_sign_up = d.pop("progressive_sign_up", UNSET)

        enhanced_email_deliverability = d.pop("enhanced_email_deliverability", UNSET)

        update_instance_auth_config_response_200 = cls(
            object_=object_,
            id=id,
            restricted_to_allowlist=restricted_to_allowlist,
            from_email_address=from_email_address,
            progressive_sign_up=progressive_sign_up,
            enhanced_email_deliverability=enhanced_email_deliverability,
        )

        update_instance_auth_config_response_200.additional_properties = d
        return update_instance_auth_config_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
