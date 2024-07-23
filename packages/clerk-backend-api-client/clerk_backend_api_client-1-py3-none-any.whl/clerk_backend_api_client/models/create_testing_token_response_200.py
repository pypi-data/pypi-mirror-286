from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_testing_token_response_200_object import CreateTestingTokenResponse200Object

T = TypeVar("T", bound="CreateTestingTokenResponse200")


@_attrs_define
class CreateTestingTokenResponse200:
    """
    Attributes:
        object_ (CreateTestingTokenResponse200Object):
        token (str): The actual token. This value is meant to be passed in the `__clerk_testing_token` query parameter
            with requests to the Frontend API. Example: 1713877200-c_2J2MvPu9PnXcuhbPZNao0LOXqK9A7YrnBn0HmIWxy.
        expires_at (int): Unix timestamp of the token's expiration time.
             Example: 1713880800.
    """

    object_: CreateTestingTokenResponse200Object
    token: str
    expires_at: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        token = self.token

        expires_at = self.expires_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "token": token,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = CreateTestingTokenResponse200Object(d.pop("object"))

        token = d.pop("token")

        expires_at = d.pop("expires_at")

        create_testing_token_response_200 = cls(
            object_=object_,
            token=token,
            expires_at=expires_at,
        )

        create_testing_token_response_200.additional_properties = d
        return create_testing_token_response_200

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
