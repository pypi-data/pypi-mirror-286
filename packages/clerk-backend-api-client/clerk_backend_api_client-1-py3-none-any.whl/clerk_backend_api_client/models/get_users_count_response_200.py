from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

from ..models.get_users_count_response_200_object import GetUsersCountResponse200Object

T = TypeVar("T", bound="GetUsersCountResponse200")


@_attrs_define
class GetUsersCountResponse200:
    """
    Attributes:
        object_ (GetUsersCountResponse200Object): String representing the object's type. Objects of the same type share
            the same value.
        total_count (int):
    """

    object_: GetUsersCountResponse200Object
    total_count: int

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        total_count = self.total_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "total_count": total_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = GetUsersCountResponse200Object(d.pop("object"))

        total_count = d.pop("total_count")

        get_users_count_response_200 = cls(
            object_=object_,
            total_count=total_count,
        )

        return get_users_count_response_200
