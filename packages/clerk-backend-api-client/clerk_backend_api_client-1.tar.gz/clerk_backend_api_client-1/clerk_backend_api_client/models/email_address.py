from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..models.email_address_object import EmailAddressObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_address_linked_to_item import EmailAddressLinkedToItem
    from ..models.email_address_verification_type_0 import EmailAddressVerificationType0
    from ..models.email_address_verification_type_1 import EmailAddressVerificationType1
    from ..models.email_address_verification_type_2 import EmailAddressVerificationType2
    from ..models.email_address_verification_type_3_type_0 import EmailAddressVerificationType3Type0
    from ..models.email_address_verification_type_3_type_1 import EmailAddressVerificationType3Type1
    from ..models.email_address_verification_type_3_type_2 import EmailAddressVerificationType3Type2
    from ..models.email_address_verification_type_4_type_0 import EmailAddressVerificationType4Type0
    from ..models.email_address_verification_type_4_type_1 import EmailAddressVerificationType4Type1
    from ..models.email_address_verification_type_4_type_2 import EmailAddressVerificationType4Type2


T = TypeVar("T", bound="EmailAddress")


@_attrs_define
class EmailAddress:
    """
    Attributes:
        object_ (EmailAddressObject): String representing the object's type. Objects of the same type share the same
            value.
        email_address (str):
        reserved (bool):
        verification (Union['EmailAddressVerificationType0', 'EmailAddressVerificationType1',
            'EmailAddressVerificationType2', 'EmailAddressVerificationType3Type0', 'EmailAddressVerificationType3Type1',
            'EmailAddressVerificationType3Type2', 'EmailAddressVerificationType4Type0',
            'EmailAddressVerificationType4Type1', 'EmailAddressVerificationType4Type2']):
        linked_to (List['EmailAddressLinkedToItem']):
        created_at (int): Unix timestamp of creation
        updated_at (int): Unix timestamp of creation
        id (Union[Unset, str]):
    """

    object_: EmailAddressObject
    email_address: str
    reserved: bool
    verification: Union[
        "EmailAddressVerificationType0",
        "EmailAddressVerificationType1",
        "EmailAddressVerificationType2",
        "EmailAddressVerificationType3Type0",
        "EmailAddressVerificationType3Type1",
        "EmailAddressVerificationType3Type2",
        "EmailAddressVerificationType4Type0",
        "EmailAddressVerificationType4Type1",
        "EmailAddressVerificationType4Type2",
    ]
    linked_to: List["EmailAddressLinkedToItem"]
    created_at: int
    updated_at: int
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.email_address_verification_type_0 import EmailAddressVerificationType0
        from ..models.email_address_verification_type_1 import EmailAddressVerificationType1
        from ..models.email_address_verification_type_2 import EmailAddressVerificationType2
        from ..models.email_address_verification_type_3_type_0 import EmailAddressVerificationType3Type0
        from ..models.email_address_verification_type_3_type_1 import EmailAddressVerificationType3Type1
        from ..models.email_address_verification_type_3_type_2 import EmailAddressVerificationType3Type2
        from ..models.email_address_verification_type_4_type_0 import EmailAddressVerificationType4Type0
        from ..models.email_address_verification_type_4_type_1 import EmailAddressVerificationType4Type1

        object_ = self.object_.value

        email_address = self.email_address

        reserved = self.reserved

        verification: Dict[str, Any]
        if isinstance(self.verification, EmailAddressVerificationType0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, EmailAddressVerificationType1):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, EmailAddressVerificationType2):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, EmailAddressVerificationType3Type0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, EmailAddressVerificationType3Type1):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, EmailAddressVerificationType3Type2):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, EmailAddressVerificationType4Type0):
            verification = self.verification.to_dict()
        elif isinstance(self.verification, EmailAddressVerificationType4Type1):
            verification = self.verification.to_dict()
        else:
            verification = self.verification.to_dict()

        linked_to = []
        for linked_to_item_data in self.linked_to:
            linked_to_item = linked_to_item_data.to_dict()
            linked_to.append(linked_to_item)

        created_at = self.created_at

        updated_at = self.updated_at

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "email_address": email_address,
                "reserved": reserved,
                "verification": verification,
                "linked_to": linked_to,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.email_address_linked_to_item import EmailAddressLinkedToItem
        from ..models.email_address_verification_type_0 import EmailAddressVerificationType0
        from ..models.email_address_verification_type_1 import EmailAddressVerificationType1
        from ..models.email_address_verification_type_2 import EmailAddressVerificationType2
        from ..models.email_address_verification_type_3_type_0 import EmailAddressVerificationType3Type0
        from ..models.email_address_verification_type_3_type_1 import EmailAddressVerificationType3Type1
        from ..models.email_address_verification_type_3_type_2 import EmailAddressVerificationType3Type2
        from ..models.email_address_verification_type_4_type_0 import EmailAddressVerificationType4Type0
        from ..models.email_address_verification_type_4_type_1 import EmailAddressVerificationType4Type1
        from ..models.email_address_verification_type_4_type_2 import EmailAddressVerificationType4Type2

        d = src_dict.copy()
        object_ = EmailAddressObject(d.pop("object"))

        email_address = d.pop("email_address")

        reserved = d.pop("reserved")

        def _parse_verification(
            data: object,
        ) -> Union[
            "EmailAddressVerificationType0",
            "EmailAddressVerificationType1",
            "EmailAddressVerificationType2",
            "EmailAddressVerificationType3Type0",
            "EmailAddressVerificationType3Type1",
            "EmailAddressVerificationType3Type2",
            "EmailAddressVerificationType4Type0",
            "EmailAddressVerificationType4Type1",
            "EmailAddressVerificationType4Type2",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_0 = EmailAddressVerificationType0.from_dict(data)

                return verification_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_1 = EmailAddressVerificationType1.from_dict(data)

                return verification_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_2 = EmailAddressVerificationType2.from_dict(data)

                return verification_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_3_type_0 = EmailAddressVerificationType3Type0.from_dict(data)

                return verification_type_3_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_3_type_1 = EmailAddressVerificationType3Type1.from_dict(data)

                return verification_type_3_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_3_type_2 = EmailAddressVerificationType3Type2.from_dict(data)

                return verification_type_3_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_4_type_0 = EmailAddressVerificationType4Type0.from_dict(data)

                return verification_type_4_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_4_type_1 = EmailAddressVerificationType4Type1.from_dict(data)

                return verification_type_4_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            verification_type_4_type_2 = EmailAddressVerificationType4Type2.from_dict(data)

            return verification_type_4_type_2

        verification = _parse_verification(d.pop("verification"))

        linked_to = []
        _linked_to = d.pop("linked_to")
        for linked_to_item_data in _linked_to:
            linked_to_item = EmailAddressLinkedToItem.from_dict(linked_to_item_data)

            linked_to.append(linked_to_item)

        created_at = d.pop("created_at")

        updated_at = d.pop("updated_at")

        id = d.pop("id", UNSET)

        email_address = cls(
            object_=object_,
            email_address=email_address,
            reserved=reserved,
            verification=verification,
            linked_to=linked_to,
            created_at=created_at,
            updated_at=updated_at,
            id=id,
        )

        return email_address
