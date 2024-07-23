from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.upload_organization_logo_response_403_errors_item import UploadOrganizationLogoResponse403ErrorsItem
    from ..models.upload_organization_logo_response_403_meta import UploadOrganizationLogoResponse403Meta


T = TypeVar("T", bound="UploadOrganizationLogoResponse403")


@_attrs_define
class UploadOrganizationLogoResponse403:
    """
    Attributes:
        errors (List['UploadOrganizationLogoResponse403ErrorsItem']):
        meta (Union[Unset, UploadOrganizationLogoResponse403Meta]):
    """

    errors: List["UploadOrganizationLogoResponse403ErrorsItem"]
    meta: Union[Unset, "UploadOrganizationLogoResponse403Meta"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        errors = []
        for errors_item_data in self.errors:
            errors_item = errors_item_data.to_dict()
            errors.append(errors_item)

        meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "errors": errors,
            }
        )
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.upload_organization_logo_response_403_errors_item import (
            UploadOrganizationLogoResponse403ErrorsItem,
        )
        from ..models.upload_organization_logo_response_403_meta import UploadOrganizationLogoResponse403Meta

        d = src_dict.copy()
        errors = []
        _errors = d.pop("errors")
        for errors_item_data in _errors:
            errors_item = UploadOrganizationLogoResponse403ErrorsItem.from_dict(errors_item_data)

            errors.append(errors_item)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, UploadOrganizationLogoResponse403Meta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = UploadOrganizationLogoResponse403Meta.from_dict(_meta)

        upload_organization_logo_response_403 = cls(
            errors=errors,
            meta=meta,
        )

        upload_organization_logo_response_403.additional_properties = d
        return upload_organization_logo_response_403

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
