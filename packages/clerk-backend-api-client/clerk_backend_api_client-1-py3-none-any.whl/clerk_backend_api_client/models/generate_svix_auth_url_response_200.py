from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="GenerateSvixAuthURLResponse200")


@_attrs_define
class GenerateSvixAuthURLResponse200:
    """
    Attributes:
        svix_url (str):
    """

    svix_url: str

    def to_dict(self) -> Dict[str, Any]:
        svix_url = self.svix_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "svix_url": svix_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        svix_url = d.pop("svix_url")

        generate_svix_auth_url_response_200 = cls(
            svix_url=svix_url,
        )

        return generate_svix_auth_url_response_200
