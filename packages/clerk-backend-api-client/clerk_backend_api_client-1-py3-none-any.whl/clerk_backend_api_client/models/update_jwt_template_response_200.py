from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..models.update_jwt_template_response_200_object import UpdateJWTTemplateResponse200Object
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_jwt_template_response_200_claims import UpdateJWTTemplateResponse200Claims


T = TypeVar("T", bound="UpdateJWTTemplateResponse200")


@_attrs_define
class UpdateJWTTemplateResponse200:
    """
    Attributes:
        object_ (UpdateJWTTemplateResponse200Object):
        id (str):
        name (str):
        claims (UpdateJWTTemplateResponse200Claims):
        lifetime (int):
        allowed_clock_skew (int):
        created_at (int): Unix timestamp of creation.
        updated_at (int): Unix timestamp of last update.
        custom_signing_key (Union[Unset, bool]):
        signing_algorithm (Union[Unset, str]):
    """

    object_: UpdateJWTTemplateResponse200Object
    id: str
    name: str
    claims: "UpdateJWTTemplateResponse200Claims"
    lifetime: int
    allowed_clock_skew: int
    created_at: int
    updated_at: int
    custom_signing_key: Union[Unset, bool] = UNSET
    signing_algorithm: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        id = self.id

        name = self.name

        claims = self.claims.to_dict()

        lifetime = self.lifetime

        allowed_clock_skew = self.allowed_clock_skew

        created_at = self.created_at

        updated_at = self.updated_at

        custom_signing_key = self.custom_signing_key

        signing_algorithm = self.signing_algorithm

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "name": name,
                "claims": claims,
                "lifetime": lifetime,
                "allowed_clock_skew": allowed_clock_skew,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if custom_signing_key is not UNSET:
            field_dict["custom_signing_key"] = custom_signing_key
        if signing_algorithm is not UNSET:
            field_dict["signing_algorithm"] = signing_algorithm

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_jwt_template_response_200_claims import UpdateJWTTemplateResponse200Claims

        d = src_dict.copy()
        object_ = UpdateJWTTemplateResponse200Object(d.pop("object"))

        id = d.pop("id")

        name = d.pop("name")

        claims = UpdateJWTTemplateResponse200Claims.from_dict(d.pop("claims"))

        lifetime = d.pop("lifetime")

        allowed_clock_skew = d.pop("allowed_clock_skew")

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        custom_signing_key = d.pop("custom_signing_key", UNSET)

        signing_algorithm = d.pop("signing_algorithm", UNSET)

        update_jwt_template_response_200 = cls(
            object_=object_,
            id=id,
            name=name,
            claims=claims,
            lifetime=lifetime,
            allowed_clock_skew=allowed_clock_skew,
            created_at=created_at,
            updated_at=updated_at,
            custom_signing_key=custom_signing_key,
            signing_algorithm=signing_algorithm,
        )

        return update_jwt_template_response_200
