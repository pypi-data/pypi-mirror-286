from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.create_invitation_response_200_object import CreateInvitationResponse200Object
from ..models.create_invitation_response_200_status import CreateInvitationResponse200Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_invitation_response_200_public_metadata import CreateInvitationResponse200PublicMetadata


T = TypeVar("T", bound="CreateInvitationResponse200")


@_attrs_define
class CreateInvitationResponse200:
    """
    Attributes:
        object_ (CreateInvitationResponse200Object):
        id (str):
        email_address (str):
        status (CreateInvitationResponse200Status):  Example: pending.
        created_at (int): Unix timestamp of creation.
        updated_at (int): Unix timestamp of last update.
        public_metadata (Union[Unset, CreateInvitationResponse200PublicMetadata]):
        revoked (Union[Unset, bool]):
        url (Union[None, Unset, str]):
    """

    object_: CreateInvitationResponse200Object
    id: str
    email_address: str
    status: CreateInvitationResponse200Status
    created_at: int
    updated_at: int
    public_metadata: Union[Unset, "CreateInvitationResponse200PublicMetadata"] = UNSET
    revoked: Union[Unset, bool] = UNSET
    url: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        id = self.id

        email_address = self.email_address

        status = self.status.value

        created_at = self.created_at

        updated_at = self.updated_at

        public_metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.public_metadata, Unset):
            public_metadata = self.public_metadata.to_dict()

        revoked = self.revoked

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "id": id,
                "email_address": email_address,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if public_metadata is not UNSET:
            field_dict["public_metadata"] = public_metadata
        if revoked is not UNSET:
            field_dict["revoked"] = revoked
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_invitation_response_200_public_metadata import CreateInvitationResponse200PublicMetadata

        d = src_dict.copy()
        object_ = CreateInvitationResponse200Object(d.pop("object"))

        id = d.pop("id")

        email_address = d.pop("email_address")

        status = CreateInvitationResponse200Status(d.pop("status"))

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        _public_metadata = d.pop("public_metadata", UNSET)
        public_metadata: Union[Unset, CreateInvitationResponse200PublicMetadata]
        if isinstance(_public_metadata, Unset):
            public_metadata = UNSET
        else:
            public_metadata = CreateInvitationResponse200PublicMetadata.from_dict(_public_metadata)

        revoked = d.pop("revoked", UNSET)

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        create_invitation_response_200 = cls(
            object_=object_,
            id=id,
            email_address=email_address,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            public_metadata=public_metadata,
            revoked=revoked,
            url=url,
        )

        return create_invitation_response_200
